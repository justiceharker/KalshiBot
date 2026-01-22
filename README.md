# Median Regression Bot

Automated trading bot for Kalshi using median-reversion strategy. Tracks rolling median price and takes profits when price deviates above median, with time-based risk management and dynamic market filtering.

## Features
- **Median-Reversion Strategy:** Tracks a rolling window of prices and executes sells when price exceeds median + deviation threshold.
- **Market Filtering:** Only trades high-liquidity markets (configurable by open interest and spread).
- **Dynamic Position Sizing:** Scale trade size based on account balance and market volatility.
- **Volatility-Based Thresholds:** Automatically adjust deviation threshold based on price volatility.
- **Smart Entry Logic:** Avoid entering positions near market close.
- **Environment-Configurable:** All strategy params controlled via env vars.
- **Paper Trading Mode:** Test the strategy without live orders.
- **Rich Dashboard:** Real-time position tracking with profit/loss and deviation metrics.
- **Logging:** Trade execution history saved to CSV.

## Quick Start

### 1. Setup Python Environment
```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Kalshi Credentials
Create a `.env` file (or export as environment variables):
```
KALSHI_KEY_ID=your-key-id-here
KALSHI_PRIVATE_KEY_PATH=kalshi_key.pem
```

**IMPORTANT:** Never commit `kalshi_key.pem` or API keys to git. The `.gitignore` excludes these automatically.

### 3. Run in Paper Trading Mode (Test)
```powershell
$env:PAPER_TRADING="true"
python median_regression.py
```

### 4. Run Live (with real orders)
```powershell
python median_regression.py
```

## Strategy Parameters (Environment Variables)

Customize behavior by setting these before running:

### Core Strategy
| Variable | Default | Description |
|----------|---------|-------------|
| `MR_WINDOW` | 15 | Rolling window size (price samples) |
| `MR_THRESHOLD` | 5.0 | Base deviation % above median to trigger sell |
| `MR_MAX_HOLD` | 3600 | Max hold time in seconds (1 hour) |
| `MR_REFRESH` | 2 | Update frequency (seconds) |

### Market Filtering (Liquidity)
| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_OPEN_INTEREST` | 100 | Minimum shares in open interest to trade |
| `MAX_SPREAD_PCT` | 2.0 | Maximum bid-ask spread % allowed |
| `MIN_VOLUME` | 10 | Minimum recent volume to trade |

### Dynamic Position Sizing
| Variable | Default | Description |
|----------|---------|-------------|
| `POSITION_SIZING` | true | Enable dynamic position sizing |
| `BASE_POSITION_SIZE` | 1 | Base shares to buy per trade |
| `MAX_POSITION_SIZE` | 10 | Maximum shares per trade |
| `RISK_PERCENT` | 1.0 | % of account balance to risk per trade |

### Volatility-Based Thresholds
| Variable | Default | Description |
|----------|---------|-------------|
| `VOLATILITY_THRESHOLD` | true | Enable volatility-adjusted thresholds |
| `VOLATILITY_MULTIPLIER` | 1.0 | Sensitivity to volatility changes |

### Entry Logic
| Variable | Default | Description |
|----------|---------|-------------|
| `HOURS_BEFORE_CLOSE` | 2 | Don't enter positions this close to market close |

### Other
| Variable | Default | Description |
|----------|---------|-------------|
| `PAPER_TRADING` | false | Set to `true` to test without executing orders |
| `KALSHI_LOG_FILE` | trading_log.csv | Where to save trade logs |

### Example Configuration
```powershell
# Aggressive: small window, low threshold, tight spreads
$env:MR_WINDOW="10"
$env:MR_THRESHOLD="2.0"
$env:MAX_SPREAD_PCT="1.0"
$env:BASE_POSITION_SIZE="5"

# Conservative: larger window, higher threshold, high liquidity only
$env:MR_WINDOW="20"
$env:MR_THRESHOLD="8.0"
$env:MIN_OPEN_INTEREST="500"
$env:BASE_POSITION_SIZE="1"

# Run
$env:PAPER_TRADING="true"
python median_regression.py
```

## Files
- `median_regression.py` — Main trading bot (median-reversion strategy with all features).

## License
MIT — See [LICENSE](LICENSE)
