
import os
import logging
import asyncio
from flask import Flask, render_template, jsonify, Response
from src.utils.logger import get_recent_logs
from src.main import TradingBot
from config.settings import (INSTRUMENT, TIMEFRAME_SECONDS, OPTION_DURATION, 
                           OPTION_DURATION_UNIT, STAKE_AMOUNT, CURRENCY)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Create single bot instance
bot = TradingBot()

@app.route('/')
def index():
    """Render the main trading bot control panel."""
    logger.debug("Rendering index page")
    return render_template('index.html')

@app.route('/start_bot')
def start_bot():
    """Start the trading bot if not already running."""
    status = bot.get_status()
    if status['is_running']:
        return jsonify({"status": "Bot already running"})
    
    # Create task to start bot asynchronously
    asyncio.create_task(bot.start())
    return jsonify({"status": "Bot started"})

@app.route('/stop_bot')
def stop_bot():
    """Stop the trading bot."""
    asyncio.run(bot.stop())
    return jsonify({"status": "Bot stopped"})

@app.route('/stream_logs')
def stream_logs():
    """Stream logs using Server-Sent Events"""
    def generate():
        last_id = 0
        while True:
            new_logs = get_recent_logs(last_id)
            if new_logs:
                last_id = len(get_recent_logs()) - 1
                data = "data: " + jsonify(new_logs).get_data(as_text=True) + "\n\n"
                yield data
            yield ":\n\n"  # Keep-alive

    return Response(generate(), mimetype='text/event-stream')

@app.route('/get_status')
def get_status():
    """Get current bot status and configuration."""
    status = bot.get_status()
    
    # Get balance if API is connected
    balance = "N/A"
    if bot.is_running and bot.api:
        try:
            balance_result = asyncio.run(bot.api.balance())
            if balance_result and 'balance' in balance_result:
                balance = f"{balance_result['balance']} {CURRENCY}"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
