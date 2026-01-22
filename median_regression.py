import time
import os
import csv
import datetime
from collections import deque
from statistics import median
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

# Configuration via environment variables (safer than hardcoding)
KEY_ID = os.getenv("KALSHI_KEY_ID")
PRIVATE_KEY_PATH = os.getenv("KALSHI_PRIVATE_KEY_PATH", "kalshi_key.pem")
LOG_FILE = os.getenv("KALSHI_LOG_FILE", "trading_log.csv")
PAPER_TRADING = os.getenv("PAPER_TRADING", "false").lower() in ("1", "true", "yes")

# Strategy parameters
ROLLING_WINDOW = int(os.getenv("MR_WINDOW", "15"))
DEVIATION_THRESHOLD_PCT = float(os.getenv("MR_THRESHOLD", "5.0"))  # percent
MAX_HOLD_SECONDS = int(os.getenv("MR_MAX_HOLD", str(60 * 60)))  # 1 hour
REFRESH_RATE = float(os.getenv("MR_REFRESH", "2"))

console = Console()

# Try to initialize Kalshi client if available; remain tolerant if not running live
client = None
try:
    from kalshi_python_sync import Configuration, KalshiClient
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()
    config = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
    if KEY_ID:
        config.api_key_id = KEY_ID
    config.private_key_pem = private_key
    client = KalshiClient(config)
except Exception as e:
    console.print(f"[yellow]Warning: Kalshi client not configured or key missing: {e}[/yellow]")


def log_trade(ticker, title, entry, exit_price, pnl_pct, reason):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Ticker", "Event", "Entry", "Exit", "PnL%", "Reason", "Mode"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        mode = "SIMULATED" if PAPER_TRADING else "LIVE"
        writer.writerow([timestamp, ticker, title, f"${entry:.2f}", f"${exit_price:.2f}", f"{pnl_pct:.1f}%", reason, mode])


def execute_order(ticker, shares, reason, action="sell"):
    if PAPER_TRADING or client is None:
        console.print(f"[yellow]SIMULATED {action.upper()} {ticker} {shares} — {reason}[/yellow]")
        return True
    try:
        client.create_order(ticker=ticker, action=action, count=shares, type="market", side="yes")
        console.print(f"[green]LIVE {action.upper()} {ticker} {shares} — {reason}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Order failed: {e}[/red]")
        return False


def get_market_price(ticker):
    if client is None:
        return None
    try:
        r = client.get_market(ticker)
        m = r.market
        return float(m.yes_bid_dollars)
    except Exception:
        return None


def generate_dashboard(rows):
    table = Table(title="Median Regression Bot — Positions")
    table.add_column("Ticker")
    table.add_column("Entry", justify="right")
    table.add_column("Now", justify="right")
    table.add_column("Median", justify="right")
    table.add_column("Dev%", justify="right")
    table.add_column("PnL%", justify="right")
    table.add_column("Hold")
    for r in rows:
        table.add_row(r["ticker"], f"${r['entry']:.2f}", f"${r['now']:.2f}", f"${r['median']:.2f}", f"{r['dev']:+.2f}%", f"{r['pnl']:+.1f}%", f"{r['hold_min']:.1f}m")
    return Panel(table)


def main_loop():
    price_hist = {}
    entry_times = {}

    with Live(generate_dashboard([]), refresh_per_second=1, screen=True) as live:
        while True:
            rows = []
            try:
                if client is None:
                    console.print("[red]No Kalshi client available; sleeping...[/red]")
                    time.sleep(5)
                    continue

                resp = client.get_positions()
                all_pos = (getattr(resp, 'market_positions', []) or []) + (getattr(resp, 'event_positions', []) or [])
                now = time.time()
                for pos in all_pos:
                    shares = abs(int(getattr(pos, 'position', 0)))
                    if shares <= 0:
                        continue
                    ticker = getattr(pos, 'ticker', getattr(pos, 'event_ticker', 'Unknown'))
                    market = client.get_market(ticker).market
                    current = float(market.yes_bid_dollars)
                    cost = getattr(pos, 'market_exposure', getattr(pos, 'total_cost', 0))
                    entry = (cost / shares) / 100 if cost > 100 else (cost / shares)

                    price_hist.setdefault(ticker, deque(maxlen=ROLLING_WINDOW))
                    price_hist[ticker].append(current)
                    med = median(list(price_hist[ticker])) if len(price_hist[ticker]) >= 3 else current
                    dev_pct = (current - med) / med * 100 if med != 0 else 0.0
                    pnl = ((current - entry) / entry * 100) if entry > 0 else 0.0

                    if ticker not in entry_times:
                        entry_times[ticker] = now
                    hold_sec = now - entry_times[ticker]

                    # Median-reversion sell rules
                    sold = False
                    reason = None
                    if dev_pct >= DEVIATION_THRESHOLD_PCT and pnl > 0:
                        reason = f"Above median +{DEVIATION_THRESHOLD_PCT}% — take profit"
                        if execute_order(ticker, shares, reason, action="sell"):
                            log_trade(ticker, market.title, entry, current, pnl, reason)
                            sold = True
                    elif hold_sec >= MAX_HOLD_SECONDS:
                        reason = f"Max hold time exceeded ({MAX_HOLD_SECONDS}s)"
                        if execute_order(ticker, shares, reason, action="sell"):
                            log_trade(ticker, market.title, entry, current, pnl, reason)
                            sold = True

                    if sold:
                        # remove tracking
                        if ticker in price_hist:
                            del price_hist[ticker]
                        if ticker in entry_times:
                            del entry_times[ticker]
                        continue

                    rows.append({
                        "ticker": ticker,
                        "entry": entry,
                        "now": current,
                        "median": med,
                        "dev": dev_pct,
                        "pnl": pnl,
                        "hold_min": hold_sec / 60.0,
                    })

                live.update(generate_dashboard(rows))
                time.sleep(REFRESH_RATE)

            except KeyboardInterrupt:
                console.print("[yellow]Stopped by user[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                time.sleep(3)


if __name__ == "__main__":
    console.print("[cyan]Starting Median Regression Bot[/cyan]")
    main_loop()
