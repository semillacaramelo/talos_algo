import asyncio
import pandas as pd
import inspect
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger()

# Module-level handler (keep for potential use with manager)
async def _tick_handler(message):
    try:
        tick_data = message.get('tick', {})
        if tick_data:
            logger.info(f"Tick Handler Received: {tick_data}")
        else:
            logger.debug(f"Tick Handler Received non-tick message: {message}")
    except Exception as e:
        logger.exception("Error in _tick_handler")

async def get_historical_data(api, instrument, granularity, count):
    """
    Fetch historical data for a given instrument.

    Parameters:
        api: Connected Deriv API object.
        instrument (str): The trading instrument symbol.
        granularity (int): Timeframe in seconds (e.g., 60 for 1-minute candles).
        count (int): Number of historical bars to fetch.

    Returns:
        pd.DataFrame: Historical data as a pandas DataFrame.
    """
    try:
        logger.info(f"Fetching historical data for {instrument} with granularity {granularity} and count {count}...")

        # Validate parameters
        if not instrument or not granularity or not count:
            raise ValueError("Invalid parameters for historical data request.")

        # Fetch historical data from the API
        response = await api.ticks_history({
            "ticks_history": instrument,
            "end": "latest",
            "count": count,
            "style": "candles",
            "granularity": granularity
        })

        # Check if response contains data
        if "candles" not in response or not response["candles"]:
            logger.warning(f"No historical data returned for {instrument}. Response: {response}")
            return pd.DataFrame()

        # Convert response to pandas DataFrame
        candles = response["candles"]
        df = pd.DataFrame(candles)

        # Rename columns for clarity
        df.rename(columns={"epoch": "time", "open": "open", "high": "high", "low": "low", "close": "close"}, inplace=True)

        # Convert epoch time to datetime
        df["time"] = pd.to_datetime(df["time"], unit="s")

        logger.info(f"Successfully fetched {len(df)} historical data points for {instrument}.")
        return df

    except Exception as e:
        logger.exception("Error fetching historical data")
        return pd.DataFrame()

async def subscribe_to_ticks(api, instrument):
    """
    Subscribe to tick data using the SubscriptionManager.

    Parameters:
        api: Connected Deriv API object.
        instrument (str): The trading instrument symbol.

    Returns:
        dict: Dictionary containing the observable and disposable subscription objects, or None on error.
    """
    try:
        logger.info(f"Attempting to subscribe via SubscriptionManager for {instrument}...")

        # Access the subscription manager
        manager = api.subscription_manager

        # Inspect the manager's subscribe method signature if needed
        try:
            sig = inspect.signature(manager.subscribe)
            logger.info(f"Inspect Signature of manager.subscribe: {sig}")
        except Exception as inspect_e:
            logger.error(f"Could not inspect manager.subscribe signature: {inspect_e}")

        # Import here to avoid circular imports
        from src.main import handle_tick

        # Define observer callbacks
        def on_tick(message):
            if isinstance(message, dict) and 'tick' in message:
                # Use the handle_tick function from main.py to process the tick
                handle_tick(message)
            else:
                logger.debug(f"Received non-tick message: {message}")

        def on_error(error):
            logger.error(f"Observable error: {error}")

        def on_completed():
            logger.info("Observable stream completed.")

        # Subscribe using the manager - returns an Observable
        # Properly await the coroutine
        observable = await manager.subscribe({"ticks": instrument})

        # Add our observer to the Observable
        disposable = observable.subscribe(
            on_next=on_tick,
            on_error=on_error,
            on_completed=on_completed
        )

        logger.info(f"SubscriptionManager.subscribe returned type: {type(observable)}")
        logger.info(f"Successfully initiated tick stream via SubscriptionManager for {instrument}.")
        
        # Return both the observable and its disposable for management
        return {
            'observable': observable,
            'disposable': disposable
        }

    except AttributeError as e:
        logger.error(f"Could not find api.subscription_manager or its subscribe method: {e}")
        return None
    except TypeError as e:
        logger.exception(f"TypeError during SubscriptionManager subscribe call: {e}. Request: {{'ticks': instrument}}")
        return None
    except Exception as e:
        logger.exception(f"Error subscribing via SubscriptionManager for {instrument}")
        return None