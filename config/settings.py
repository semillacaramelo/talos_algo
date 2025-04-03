import os

# Read environment variables
API_TOKEN = os.environ.get('DERIV_DEMO_API_TOKEN')
APP_ID = os.environ.get('DERIV_APP_ID')

# Validate API_TOKEN
if not API_TOKEN:
    raise Exception("Error: DERIV_DEMO_API_TOKEN environment variable is not set or empty.")

# Warn if APP_ID is not set
if not APP_ID:
    print("Warning: DERIV_APP_ID environment variable is not set. It might be required for some API operations.")

# Trading strategy configuration
INSTRUMENT = "R_100"  # Example: Volatility 100 Index
TIMEFRAME_SECONDS = 60  # 1-minute candles
HISTORICAL_BARS_COUNT = 100  # Number of past candles for analysis or training

# Digital Options Trading Configuration
OPTION_DURATION = 1  # Duration quantity (changed from 5 to 1 minute)
OPTION_DURATION_UNIT = 'm'  # Duration unit: 't' for ticks, 's' for seconds, 'm' for minutes
STAKE_AMOUNT = 1.0  # Amount for stake (increased from 0.40 to avoid API issues)
BASIS = 'stake'  # 'stake' or 'payout'
CURRENCY = 'USD'  # Account currency

# Risk Management
MAX_CONCURRENT_TRADES = 1  # Maximum number of concurrent open trades