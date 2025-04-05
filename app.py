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
    
    # Use the thread-safe method to check if bot is running
    if bot.get_running_status():
        logger.info("Bot already running")
        return jsonify({"status": "Bot is already running"})
    
    # Start bot
    success = await bot.start()
    logger.info(f"Bot start initiated: {success}")
    return jsonify({"status": "Bot started"})

@app.route('/stop_bot')
@async_route
async def stop_bot():
    """Stop the trading bot."""
    logger.info("Received stop bot request")
    
    # Check if bot is actually running using thread-safe method
    if not bot.get_running_status():
        logger.info("Bot already stopped")
        return jsonify({"status": "Bot is not currently running"})
        
    try:
        # Call the stop method with proper exception handling
        success = await bot.stop()
        
        # Give a short delay to allow async operations to complete
        await asyncio.sleep(0.5)
        
        # Double-check that it actually stopped
        if success:
            logger.info("Bot stop successful")
            return jsonify({"status": "Bot stopping"})
        else:
            logger.error("Bot stop unsuccessful")
            return jsonify({"status": "Failed to stop bot"}), 500
    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Error stopping bot: {e}")
        return jsonify({"status": f"Error stopping bot: {str(e)}"}), 500

@app.route('/logs')
def get_logs():
    """Get recent logs as JSON"""
    with app.app_context():
        logs = get_recent_logs()
        return jsonify(logs)

@app.route('/stream_logs')
def stream_logs():
    """Stream logs using Server-Sent Events (SSE) protocol."""
    from src.utils.logger import log_queue
    
    def generate():
        """Generator function to yield SSE formatted log entries."""
        # Start at the most recent position
        last_pos = len(log_queue) - 1 if log_queue else 0
        
        while True:
            # Check if there are new logs
            current_size = len(log_queue)
            if current_size > last_pos:
                # We have new logs, yield them
                for i in range(last_pos, current_size):
                    log = list(log_queue)[i]
                    data = json.dumps({
                        'timestamp': log['timestamp'],
                        'level': log['level'],
                        'message': log['message']
                    })
                    yield f"data: {data}\n\n"
                
                # Update position
                last_pos = current_size
            
            # Wait before checking again
            time.sleep(0.5)
    
    return Response(generate(), mimetype="text/event-stream")

# Note: We're changing to a polling approach for compatibility with Gunicorn
# We'll update the frontend to poll this endpoint instead of using SSE

@app.route('/get_status')
@async_route
async def get_status():
    """Get current bot status and configuration."""
    status = bot.get_status()
    
    # Initialize default values
    balance = "N/A"
    last_signal = "N/A"
    last_price = "N/A"
    feature_count = "N/A"
    last_trade = "N/A"
    uptime = "N/A"
    daily_pnl = 0.0
    win_count = 0
    loss_count = 0
    active_contracts = []
    model_status = "Not Loaded"
    model_file = "N/A"
    
    if status['is_running'] and hasattr(bot, 'api') and bot.api.api:
        try:
            # Access the underlying official API
            api = bot.api.api
            balance_response = await api.balance()
            if balance_response and 'balance' in balance_response:
                balance = f"{balance_response['balance']['currency']} {balance_response['balance']['balance']}"
                
            # Get additional bot info
            if hasattr(bot, 'last_signal'):
                last_signal = bot.last_signal or "None"
            
            if hasattr(bot, 'last_tick_price'):
                last_price = str(bot.last_tick_price) or "None"
                
            if hasattr(bot, 'feature_data_count'):
                feature_count = str(bot.feature_data_count) or "N/A"
            elif hasattr(bot, 'last_feature_count'):
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

            # Get win/loss counts and daily PnL
            if hasattr(bot, 'daily_pnl'):
                daily_pnl = bot.daily_pnl
            
            if hasattr(bot, 'win_count'):
                win_count = bot.win_count
                
            if hasattr(bot, 'loss_count'):
                loss_count = bot.loss_count
                
            if hasattr(bot, 'model_status'):
                model_status = bot.model_status
                
            # Get model file path
            if hasattr(bot, 'model') and bot.model:
                import os.path
                model_file = os.path.basename(os.path.join(os.path.dirname(__file__), 'src/models/basic_predictor.joblib'))
            
            # FIXED: Create serializable version of active contracts
            serializable_contracts = []
            if hasattr(bot, 'active_contracts') and bot.active_contracts:
                # Extract only JSON-safe data from active contracts
                for contract_id, contract_data in bot.active_contracts.items():
                    # Skip the 'subscription' which contains the non-serializable Disposable object
                    safe_contract = {
                        "id": contract_id,
                        "type": contract_data.get('type', 'UNKNOWN'),
                        "stake": contract_data.get('stake', 0),
                        "entry_time": str(contract_data.get('entry_time', 'N/A')),
                    }
                    
                    # Include any safe nested details if present
                    if 'details' in contract_data and isinstance(contract_data['details'], dict):
                        details = contract_data['details']
                        safe_contract.update({
                            "entry_price": details.get('entry_price', 'N/A'),
                            "current_price": details.get('current_price', 'N/A'),
                            "pnl": details.get('profit', 0)
                        })
                    
                    serializable_contracts.append(safe_contract)
                
            # Set active contracts for UI
            active_contracts = serializable_contracts
                    
        except Exception as e:
            logger.error(f"Error fetching extended status: {e}")
    
    # Add MAX_CONCURRENT_TRADES to config
    from config.settings import MAX_CONCURRENT_TRADES, INSTRUMENT, OPTION_DURATION, OPTION_DURATION_UNIT, STAKE_AMOUNT, CURRENCY
    
    # Calculate win rate
    win_rate = 0
    total_trades = win_count + loss_count
    if total_trades > 0:
        win_rate = (win_count / total_trades) * 100
    
    return jsonify({
        "status": "Running" if status['is_running'] else "Idle",
        "balance": balance,
        "active_trades": len(active_contracts),
        "last_signal": last_signal,
        "last_price": last_price,
        "feature_count": feature_count,
        "last_trade": last_trade,
        "uptime": uptime,
        "daily_pnl": daily_pnl,
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate": win_rate,
        "model_status": model_status,
        "model_file": model_file,
        "trades": active_contracts,
        "config": {
            "instrument": INSTRUMENT,
            "duration": OPTION_DURATION,
            "duration_unit": OPTION_DURATION_UNIT,
            "stake": STAKE_AMOUNT,
            "currency": CURRENCY,
            "max_concurrent_trades": MAX_CONCURRENT_TRADES
        }
    })

@app.route('/update_settings', methods=['POST'])
@async_route
async def update_settings():
    """Update the bot's configuration settings."""
    from flask import request
    
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        logger.info(f"Received settings update: {data}")
        
        # Import settings module for potential updates
        import config.settings
        import importlib
        
        # Track which settings are being updated
        updated_settings = []
        restart_required = False
        
        # Update instrument if provided
        if 'instrument' in data and data['instrument']:
            old_instrument = config.settings.INSTRUMENT
            # Validate instrument format
            if isinstance(data['instrument'], str) and len(data['instrument']) > 0:
                config.settings.INSTRUMENT = data['instrument']
                updated_settings.append(f"Instrument: {old_instrument} → {data['instrument']}")
                
                # If bot is running, this will require a restart
                if bot.get_running_status():
                    restart_required = True
        
        # Update duration if provided
        if 'duration' in data and data['duration']:
            try:
                duration = int(data['duration'])
                old_duration = config.settings.OPTION_DURATION
                config.settings.OPTION_DURATION = duration
                updated_settings.append(f"Duration: {old_duration} → {duration}")
            except (ValueError, TypeError):
                logger.warning(f"Invalid duration value: {data['duration']}")
        
        # Update duration unit if provided
        if 'duration_unit' in data and data['duration_unit']:
            old_unit = config.settings.OPTION_DURATION_UNIT
            valid_units = ['t', 's', 'm', 'h', 'd']
            if data['duration_unit'] in valid_units:
                config.settings.OPTION_DURATION_UNIT = data['duration_unit']
                updated_settings.append(f"Duration Unit: {old_unit} → {data['duration_unit']}")
        
        # Update stake amount if provided
        if 'stake' in data and data['stake']:
            try:
                stake = float(data['stake'])
                old_stake = config.settings.STAKE_AMOUNT
                if stake > 0:
                    config.settings.STAKE_AMOUNT = stake
                    updated_settings.append(f"Stake Amount: {old_stake} → {stake}")
            except (ValueError, TypeError):
                logger.warning(f"Invalid stake value: {data['stake']}")
        
        # Try to update the running bot's configuration if available
        # This is important to allow changes without requiring restart
        if bot.get_running_status() and hasattr(bot, 'update_config'):
            try:
                # Pass the updated settings to the bot
                await bot.update_config(data)
                logger.info("Updated running bot configuration")
            except Exception as e:
                logger.error(f"Error updating bot configuration: {e}")
                # If this fails, a restart will be required
                restart_required = True
        
        # Log the changes
        if updated_settings:
            logger.info(f"Updated settings: {', '.join(updated_settings)}")
            
            # Return success message with restart info
            if restart_required:
                return jsonify({
                    "success": True, 
                    "message": "Settings updated. Bot restart required for changes to take full effect.",
                    "restart_required": True,
                    "updated_settings": updated_settings
                })
            else:
                return jsonify({
                    "success": True, 
                    "message": "Settings updated successfully",
                    "restart_required": False,
                    "updated_settings": updated_settings
                })
        else:
            return jsonify({"success": False, "message": "No valid settings were updated"}), 400
            
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/get_chart_data')
@async_route
async def get_chart_data():
    """Get recent price data for charting."""
    chart_data = []
    
    try:
        # Check if bot is running and has recent tick data
        if bot.get_running_status() and hasattr(bot, 'recent_ticks_deque') and bot.recent_ticks_deque:
            # Convert the deque to a list of dictionaries suitable for charting
            for tick in bot.recent_ticks_deque:
                chart_data.append({
                    'time': tick['timestamp'],
                    'price': tick['close']
                })
            
            logger.debug(f"Returning {len(chart_data)} chart data points")
        else:
            logger.debug("No chart data available - bot not running or no data collected")
            
    except Exception as e:
        logger.error(f"Error preparing chart data: {e}")
    
    return jsonify(chart_data)

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
