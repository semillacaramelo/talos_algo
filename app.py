
import os
import logging
import asyncio
import json
import time
from functools import wraps
from flask import Flask, render_template, jsonify, Response
from src.utils.logger import get_recent_logs, setup_logger
from src.main import TradingBot
from config.settings import (INSTRUMENT, TIMEFRAME_SECONDS, OPTION_DURATION, 
                           OPTION_DURATION_UNIT, STAKE_AMOUNT, CURRENCY)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = setup_logger()

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Set up asyncio event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Helper function to run async functions in Flask routes
def async_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return asyncio.run_coroutine_threadsafe(f(*args, **kwargs), loop).result()
    return decorated_function

# Create single bot instance
bot = TradingBot()
# Initialize bot status variables
bot.is_running = False

@app.route('/')
def index():
    """Render the main trading bot control panel."""
    logger.info("Rendering index page")
    return render_template('index.html')

@app.route('/start_bot')
@async_route
async def start_bot():
    """Start the trading bot if not already running."""
    logger.info("Received start bot request")
    status = bot.get_status()
    if status['is_running']:
        logger.info("Bot already running")
        return {"status": "Bot already running"}
    
    # Start bot
    success = await bot.start()
    logger.info(f"Bot start initiated: {success}")
    return {"status": "Bot started"}

@app.route('/stop_bot')
@async_route
async def stop_bot():
    """Stop the trading bot."""
    logger.info("Received stop bot request")
    success = await bot.stop()
    logger.info(f"Bot stop initiated: {success}")
    return {"status": "Bot stopping"}

@app.route('/logs')
def get_logs():
    """Get recent logs as JSON"""
    with app.app_context():
        logs = get_recent_logs()
        return jsonify(logs)

# Note: We're changing to a polling approach for compatibility with Gunicorn
# We'll update the frontend to poll this endpoint instead of using SSE

@app.route('/get_status')
@async_route
async def get_status():
    """Get current bot status and configuration."""
    status = bot.get_status()
    
    # Get balance if API is connected and bot is running
    balance = "N/A"
    
    if status['is_running'] and hasattr(bot, 'api') and bot.api.connected:
        try:
            balance_response = await bot.api.balance()
            if balance_response and 'balance' in balance_response:
                balance = f"{balance_response['balance']['currency']} {balance_response['balance']['balance']}"
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
    
    return jsonify({
        "status": "Running" if status['is_running'] else "Idle",
        "balance": balance,
        "active_trades": status['active_contracts'],
        "config": {
            "instrument": INSTRUMENT,
            "duration": f"{OPTION_DURATION} {OPTION_DURATION_UNIT}",
            "stake": f"{STAKE_AMOUNT} {CURRENCY}"
        }
    })

# Start background tasks in a proper way
def start_background_loop():
    global loop
    asyncio.set_event_loop(loop)
    loop.run_forever()

import threading
thread = threading.Thread(target=start_background_loop, daemon=True)
thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
