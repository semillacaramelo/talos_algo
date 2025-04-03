import asyncio
from src.main import main as _main

def main():
    """
    Main entry point for the trading bot.
    Calls the async main function in src/main.py
    """
    asyncio.run(_main())