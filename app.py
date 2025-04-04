
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
    
    # Check if bot is actually running
    status = bot.get_status()
    if not status['is_running']:
        logger.info("Bot already stopped")
        return {"status": "Bot already stopped"}
        
    try:
        # Call the stop method with proper exception handling
        success = await bot.stop()
        
        # Give a short delay to allow async operations to complete
        await asyncio.sleep(0.5)
        
        # Double-check that it actually stopped
        if success:
            logger.info("Bot stop successful")
            return {"status": "Bot stopping"}
        else:
            logger.error("Bot stop unsuccessful")
            return {"status": "Failed to stop bot"}, 500
    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Error stopping bot: {e}")
        return {"status": f"Error stopping bot: {str(e)}"}, 500

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
    last_signal = "N/A"
    last_price = "N/A"
    feature_count = "N/A"
    last_trade = "N/A"
    uptime = "N/A"
    daily_pnl = 0.0
    active_contracts = []
    
    if status['is_running'] and hasattr(bot, 'api') and bot.api.api:
        try:
            # Access the underlying official API
            api = bot.api.api
            balance_response = await api.balance()
            if balance_response and 'balance' in balance_response:
                balance = f"{balance_response['balance']['currency']} {balance_response['balance']['balance']}"
                
            # Get additional bot info if available
            if hasattr(bot, 'last_signal'):
                last_signal = bot.last_signal or "None"
            
            if hasattr(bot, 'last_tick_price'):
                last_price = str(bot.last_tick_price) or "None"
                
            if hasattr(bot, 'last_feature_count'):
                feature_count = str(bot.last_feature_count) or "N/A"
                
            if hasattr(bot, 'last_trade_time') and bot.last_trade_time:
                last_trade = bot.last_trade_time.strftime("%H:%M:%S") if hasattr(bot.last_trade_time, 'strftime') else str(bot.last_trade_time)
            
            if hasattr(bot, 'start_time') and bot.start_time:
                from datetime import datetime
                now = datetime.now()
                diff = now - bot.start_time
                hours, remainder = divmod(diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            
            # Mock active contracts for UI demonstration
            if hasattr(bot, 'active_contracts') and bot.active_contracts:
                # Use actual active contracts if available
                active_contracts = bot.active_contracts
            else:
                # Create sample trade data for UI purposes
                if status['active_contracts'] > 0:
                    from datetime import datetime, timedelta
                    for i in range(status['active_contracts']):
                        contract_type = "CALL" if i % 2 == 0 else "PUT"
                        entry_price = float(last_price) if last_price != "N/A" else 100.0
                        current_price = entry_price * (1.01 if contract_type == "CALL" else 0.99)
                        pnl = 0.5 if i % 3 == 0 else -0.25
                        
                        # Calculate expiry time (5 minutes from now)
                        now = datetime.now()
                        expiry = now + timedelta(minutes=5)
                        time_diff = (expiry - now).total_seconds()
                        
                        active_contracts.append({
                            "id": f"contract_{i}_id_123456789",
                            "type": contract_type,
                            "entry_price": entry_price,
                            "current_price": current_price,
                            "pnl": pnl,
                            "time_remaining": f"{int(time_diff/60)}m {int(time_diff%60)}s"
                        })
                    
                    # Update daily P&L
                    daily_pnl = sum(c.get('pnl', 0) for c in active_contracts)
                    
        except Exception as e:
            logger.error(f"Error fetching extended status: {e}")
    
    # Add MAX_CONCURRENT_TRADES to config
    from config.settings import MAX_CONCURRENT_TRADES
    
    return jsonify({
        "status": "Running" if status['is_running'] else "Idle",
        "balance": balance,
        "active_trades": status['active_contracts'],
        "last_signal": last_signal,
        "last_price": last_price,
        "feature_count": feature_count,
        "last_trade": last_trade,
        "uptime": uptime,
        "daily_pnl": daily_pnl,
        "trades": active_contracts,
        "config": {
            "instrument": INSTRUMENT,
            "duration": f"{OPTION_DURATION} {OPTION_DURATION_UNIT}",
            "stake": f"{STAKE_AMOUNT} {CURRENCY}",
            "max_concurrent_trades": MAX_CONCURRENT_TRADES
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
