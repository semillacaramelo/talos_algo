import asyncio
from deriv_api import DerivAPI  # Adjust import based on actual library structure
from config.settings import API_TOKEN, APP_ID
from src.utils.logger import setup_logger

# Set up logger globally
logger = setup_logger()

# Define a default message handler
async def default_message_handler(message):
    # Log all incoming messages to see if ticks arrive here
    logger.debug(f"Default Handler Received Message: {message}")
    # Check if it's a tick message
    if message.get('msg_type') == 'tick':
        logger.info(f"Tick received via default handler: {message.get('tick')}")
    # Add handling for other message types if needed

async def connect_deriv_api():
    # Validate API_TOKEN
    if not API_TOKEN:
        logger.error("API_TOKEN is not set or invalid. Cannot connect to Deriv API.")
        return None

    # Instantiate DerivAPI object, potentially with a message handler
    # Check deriv-api docs for the correct way to set a default handler
    # This is a guess based on common patterns
    try:
        # Attempt 1: Pass handler during init (if supported)
        # api = DerivAPI(app_id=APP_ID, on_message=default_message_handler)
        # Attempt 2: Standard init, handler might be set later or automatically routed
        api = DerivAPI(app_id=APP_ID)
        # If the library requires explicit handler registration after init:
        # api.register_message_handler(default_message_handler) # Example, check docs

    except Exception as e:
        logger.exception("Failed to instantiate DerivAPI")
        return None

    try:
        logger.info("Attempting to connect to Deriv API...")
        await api.authorize(API_TOKEN)
        logger.info("Successfully connected and authorized with Deriv API.")
        return api
    except Exception as e:
        logger.exception("Failed to connect/authorize with Deriv API")
        # Ensure disconnection if partial connection occurred
        if api and hasattr(api, 'disconnect'):
            try:
                await disconnect(api)
            except Exception as disc_e:
                logger.exception("Error during disconnection after failed auth")
        return None

async def disconnect(api):
    """
    Safely disconnect from the Deriv API.
    
    Parameters:
        api: Connected Deriv API object.
        
    Returns:
        bool: True if disconnection was successful, False otherwise.
    """
    if not api:
        logger.warning("Cannot disconnect: API object is None")
        return False
        
    try:
        # Check if the connection is active before disconnecting
        if hasattr(api, 'is_connected') and api.is_connected():
            logger.info("Disconnecting from the Deriv API...")
            
            # Give any pending messages a moment to complete
            await asyncio.sleep(0.5)
            
            # Ensure all subscriptions are cleared before disconnect
            if hasattr(api, 'subscription_manager'):
                try:
                    await api.subscription_manager.unsubscribe_all()
                    logger.info("All subscriptions cleared.")
                except Exception as e:
                    logger.warning(f"Error clearing subscriptions: {e}")
            
            # Ensure all pending coroutines are awaited
            for _ in range(5):  # Allow for drain time to complete pending tasks
                await asyncio.sleep(0.1)
                
            # Perform the actual disconnect
            await api.disconnect()
            
            # Additional wait after disconnect to ensure everything is flushed
            await asyncio.sleep(0.2)
            
            logger.info("Successfully disconnected from the Deriv API.")
            return True
        else:
            logger.info("API connection already closed or not established.")
            return False
    except Exception as e:
        logger.exception(f"Error during API disconnection: {e}")
        return False

async def place_trade_order(api, instrument, trade_type, volume, price=None, stop_loss=None, take_profit=None):
    """
    Places a trade order via the Deriv API.

    Parameters:
        api: Connected Deriv API object.
        instrument (str): The trading instrument symbol.
        trade_type (str): 'BUY' or 'SELL'.
        volume (float): The trade volume/stake.
        price (float, optional): The price for limit orders. Defaults to None for market orders.
        stop_loss (float, optional): Stop loss price level.
        take_profit (float, optional): Take profit price level.

    Returns:
        dict: The response from the API regarding the order placement, or None on error.
    """
    try:
        # Construct the order request for CFD
        # IMPORTANT: Verify parameters against Deriv API documentation for 'buy' endpoint (CFD)
        order_request = {
            "buy": 1, # This will be overwritten by trade_type logic
            "parameters": {
                "contract_type": "CFD", # Verify exact name if needed
                "symbol": instrument,
                "volume": volume,
                # Optional parameters:
                # "price": price, # For limit orders
                # "stop_loss": stop_loss,
                # "take_profit": take_profit,
                # "leverage": 500, # Example: Add leverage if required/configurable
            },
            "price": 1 # Placeholder price, API might require proposal first for CFDs
                      # Or the 'buy' call might handle market orders directly.
                      # CONSULT API DOCS: Often requires proposal_open_contract or similar
        }

        # Set direction
        if trade_type.upper() == 'BUY':
            # Assuming buy=1 is correct for the main request structure
            pass # buy=1 is already set
        elif trade_type.upper() == 'SELL':
            # How sell is specified depends heavily on the API endpoint structure.
            # Option 1: Use sell=1 instead of buy=1
            # order_request["sell"] = 1
            # del order_request["buy"]
            # Option 2: Use a different contract type or parameter
            # order_request["parameters"]["contract_type"] = "CFD_SELL" # Fictional example
            # Option 3: The 'buy' endpoint handles both, direction inferred differently?
            # For now, we'll assume buy=1 is used and direction might be implicit or handled by SL/TP logic
            # This part NEEDS verification from Deriv API docs.
            logger.warning("SELL order logic needs verification based on Deriv API spec for CFDs.")
            # As a temporary measure, let's assume buy=1 is used and SL/TP define direction implicitly
            # This is likely INCORRECT and needs fixing based on docs.
            pass
        else:
            logger.error(f"Invalid trade type: {trade_type}")
            return None

        # Add optional parameters to the 'parameters' sub-dictionary
        if price:
            order_request["parameters"]["price"] = price
        if stop_loss:
            order_request["parameters"]["stop_loss"] = stop_loss
        if take_profit:
            order_request["parameters"]["take_profit"] = take_profit

        logger.info(f"Placing {trade_type} order for {instrument} with request: {order_request}")

        # --- CRITICAL: Verify API Call --- 
        # The 'api.buy' call might be incorrect for CFDs.
        # Often, you need to get a price proposal first (api.proposal_open_contract or similar)
        # and then use the ID from the proposal to execute the trade.
        # Replace 'api.buy' with the correct sequence based on Deriv API docs.
        # Example (Conceptual - needs correct API calls):
        # proposal = await api.proposal_open_contract(order_request['parameters'])
        # if proposal and not proposal.get('error'):
        #     proposal_id = proposal.get('proposal_open_contract', {}).get('id')
        #     if proposal_id:
        #         order_response = await api.buy({"buy": proposal_id, "price": proposal['proposal_open_contract']['ask_price'] })
        #     else: # Handle missing proposal ID
        # else: # Handle proposal error

        # Using api.buy directly as a placeholder - LIKELY NEEDS CHANGE
        order_response = await api.buy(order_request["parameters"])
        # --------------------------------

        logger.info(f"Order placement response: {order_response}")

        if order_response and not order_response.get('error'):
            logger.info("Order placed successfully (based on placeholder API call).")
            return order_response
        else:
            error_details = order_response.get('error', {})
            logger.error(f"Order placement failed: {error_details}")
            return None

    except Exception as e:
        logger.exception(f"Error placing {trade_type} order for {instrument}")
        return None