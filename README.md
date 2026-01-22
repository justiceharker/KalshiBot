# KalshiBot

Automated helper for managing Kalshi market positions (autosell and logging).

Files
- `autosell.py` — main script for automatic selling logic.
- `trading_log.csv` — execution log (ignored by git).

Quick start
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

2. Install dependencies (add `requirements.txt` later):

```powershell
pip install -r requirements.txt
```

3. Run the bot:

```powershell
python autosell.py
```

Notes
- This repository currently contains the core script and logs. Consider adding `requirements.txt`, `LICENSE` (MIT recommended), and CI for tests.
