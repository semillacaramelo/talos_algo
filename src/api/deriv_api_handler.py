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

async def get_option_proposal(api, instrument, contract_type, duration, duration_unit, currency, amount, basis):
    """
    Get a price proposal for a digital option contract.
    
    Parameters:
        api: Connected Deriv API object.
        instrument (str): Trading instrument symbol.
        contract_type (str): "CALL" for Rise prediction or "PUT" for Fall prediction.
        duration (int): The contract duration.
        duration_unit (str): The contract duration unit ('t' for ticks, 's' for seconds, 'm' for minutes).
        currency (str): The currency for the proposal.
        amount (float): The stake amount.
        basis (str): The basis for the proposal ("stake" or "payout").
        
    Returns:
        dict: The proposal response from the API, or None on error.
    """
    try:
        # Ensure amount is a float and duration is an integer
        amount = float(amount)
        duration = int(duration)
        
        # Construct the proposal request for a digital option
        proposal_request = {
            "proposal": 1,
            "amount": amount,
            "basis": basis,
            "contract_type": contract_type,
            "currency": currency,
            "duration": duration,
            "duration_unit": duration_unit,
            "symbol": instrument,
        }
        
        logger.info(f"Requesting option proposal: {instrument} {contract_type} {duration}{duration_unit} {basis}:{amount} {currency}")
        
        # Send the proposal request
        proposal_response = await api.proposal(proposal_request)
        
        # Check for errors
        if proposal_response and proposal_response.get('error'):
            error_details = proposal_response.get('error', {})
            logger.error(f"Option proposal failed: {error_details}")
            return None
        
        # Log successful proposal
        if proposal_response and proposal_response.get('proposal'):
            proposal = proposal_response.get('proposal')
            logger.info(f"Option proposal successful - ID: {proposal.get('id')}, " 
                       f"Price: {proposal.get('ask_price')}, Payout: {proposal.get('payout')}")
        
        return proposal_response
        
    except Exception as e:
        logger.exception(f"Error requesting option proposal for {instrument} {contract_type}")
        return None

async def buy_option_contract(api, proposal_id, price):
    """
    Buy a digital option contract using a proposal ID.
    
    Parameters:
        api: Connected Deriv API object.
        proposal_id (str): The proposal ID from a successful proposal request.
        price (float): The price from the proposal.
        
    Returns:
        dict: The buy confirmation response from the API, or None on error.
    """
    try:
        # Create the buy request
        buy_request = {
            "buy": proposal_id,
            "price": price
        }
        
        logger.info(f"Buying contract with proposal ID: {proposal_id[:8]}... at price: {price}")
        
        # Send the buy request
        buy_response = await api.buy(buy_request)
        
        # Check for errors
        if buy_response and buy_response.get('error'):
            error_details = buy_response.get('error', {})
            logger.error(f"Contract purchase failed: {error_details}")
            return None
        
        # Log successful purchase
        if buy_response and buy_response.get('buy'):
            contract_info = buy_response.get('buy')
            logger.info(f"Contract purchased successfully - Contract ID: {contract_info.get('contract_id')}, "
                       f"Purchase Time: {contract_info.get('purchase_time')}, "
                       f"Balance After: {contract_info.get('balance_after')}")
        
        return buy_response
        
    except Exception as e:
        logger.exception(f"Error buying option contract with proposal ID {proposal_id[:8]}...")
        return None

async def subscribe_to_contract_updates(api, contract_id, on_update_callback):
    """
    Subscribe to real-time updates for a specific contract.
    
    Parameters:
        api: Connected Deriv API object.
        contract_id (str/int): The ID of the contract to monitor.
        on_update_callback (callable): Function to handle update messages.
        
    Returns:
        object: The disposable subscription object, or None on error.
    """
    try:
        logger.info(f"Attempting to subscribe to contract updates for contract ID: {contract_id}")
        
        # Access the subscription manager
        manager = api.subscription_manager
        
        # Construct the subscription request
        request = {
            "proposal_open_contract": 1,
            "contract_id": contract_id
        }
        
        # Subscribe using the manager - returns an Observable
        observable = await manager.subscribe(request)
        
        # Define observer callbacks
        def on_error(error):
            logger.error(f"Observable error for contract {contract_id}: {error}")
            
        def on_completed():
            logger.info(f"Observable stream for contract {contract_id} completed.")
        
        # Add our observer to the Observable
        disposable = observable.subscribe(
            on_next=on_update_callback,
            on_error=on_error,
            on_completed=on_completed
        )
        
        logger.info(f"Successfully initiated subscription for contract ID: {contract_id}")
        
        # Return the disposable for later cleanup
        return disposable
        
    except Exception as e:
        logger.exception(f"Error subscribing to contract updates for contract ID: {contract_id}")
        return None