import os
import logging
from flask import Flask, render_template, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Mock data for placeholders
mock_config = {
    "instrument": "BTC/USD",
    "duration": "1 hour",
    "stake": "100 USD"
}

mock_logs = [
    "Bot initialized...",
    "Waiting for actions..."
]

# Routes
@app.route('/')
def index():
    """Render the main trading bot control panel."""
    logger.debug("Rendering index page")
    return render_template('index.html')

@app.route('/start_bot')
def start_bot():
    """Placeholder route for starting the trading bot."""
    logger.debug("Start bot endpoint called")
    return jsonify({"status": "Starting bot..."})

@app.route('/stop_bot')
def stop_bot():
    """Placeholder route for stopping the trading bot."""
    logger.debug("Stop bot endpoint called")
    return jsonify({"status": "Stopping bot..."})

@app.route('/get_status')
def get_status():
    """Placeholder route for getting the current bot status."""
    logger.debug("Get status endpoint called")
    return jsonify({
        "status": "Idle",
        "balance": "N/A",
        "active_trades": 0,
        "config": mock_config
    })

@app.route('/get_logs')
def get_logs():
    """Placeholder route for getting bot logs."""
    logger.debug("Get logs endpoint called")
    return jsonify({"logs": mock_logs})
