import asyncio
import json
from config.settings import API_TOKEN, APP_ID
from src.utils.logger import setup_logger
from deriv_api import DerivAPI  # Import the official Deriv API library

# Set up logger globally
logger = setup_logger()

# Create a wrapper class for Deriv API with async functionality

class DerivAPIWrapper:
    """Wrapper class to simplify DerivAPI usage"""
    def __init__(self, api_key=API_TOKEN):
        self.api_key = api_key
        self.api = None
        
    async def connect(self):
        """Connect to the Deriv API"""
        try:
            # Create DerivAPI instance from the official library
            self.api = DerivAPI(app_id=APP_ID)
            logger.info(f"Connected to Deriv API with app ID: {APP_ID}")
            
            # Authenticate if token is provided
            if self.api_key:
                auth_response = await self.api.authorize(self.api_key)
                logger.info(f"Authorized with account: {auth_response.get('authorize', {}).get('email')}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Deriv API: {e}")
            return False
        
    async def disconnect(self):
        """Disconnect from the Deriv API"""
        try:
            # The DerivAPI library handles cleanup automatically
            if self.api:
                await self.api.clear()
                logger.info("Disconnected from Deriv API")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from Deriv API: {e}")
            return False
# The DerivAPIAsync class has been replaced with the official Deriv API library (deriv_api.DerivAPI)

# Define a default message handler
async def default_message_handler(message):
    """Handle incoming messages from the Deriv API."""
    # Log all incoming messages to see if ticks arrive here
    logger.debug(f"Default Handler Received Message: {message}")
    # Check if it's a tick message
    if message.get('msg_type') == 'tick':
        logger.info(f"Tick received via default handler: {message.get('tick')}")
    # Add handling for other message types if needed

async def get_option_proposal(api_wrapper, instrument, contract_type, duration, duration_unit, currency, amount, basis):
    """
    Get a price proposal for a digital option contract.
    
    Parameters:
        api_wrapper: Connected DerivAPIWrapper object.
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
        # Ensure we access the underlying API object
        api = api_wrapper.api
        if not api:
            logger.error("API not initialized. Call connect() first.")
            return None
            
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
        
        # Send the proposal request using the official API
        response = await api.proposal(proposal_request)
        
        # Check for errors
        if response and 'error' in response:
            error_details = response.get('error', {})
            logger.error(f"Option proposal failed: {error_details}")
            return None
        
        # Log successful proposal
        if response and 'proposal' in response:
            proposal = response.get('proposal')
            logger.info(f"Option proposal successful - ID: {proposal.get('id')}, " 
                       f"Price: {proposal.get('ask_price')}, Payout: {proposal.get('payout')}")
        
        return response
        
    except Exception as e:
        logger.exception(f"Error requesting option proposal for {instrument} {contract_type}: {e}")
        return None

async def buy_option_contract(api_wrapper, proposal_id, price):
    """
    Buy a digital option contract using a proposal ID.
    
    Parameters:
        api_wrapper: Connected DerivAPIWrapper object.
        proposal_id (str): The proposal ID from a successful proposal request.
        price (float): The price from the proposal.
        
    Returns:
        dict: The buy confirmation response from the API, or None on error.
    """
    try:
        # Ensure we access the underlying API object
        api = api_wrapper.api
        if not api:
            logger.error("API not initialized. Call connect() first.")
            return None
            
        # Create the buy request
        buy_request = {
            "buy": proposal_id,
            "price": float(price)
        }
        
        id_preview = proposal_id[:8] if len(proposal_id) > 8 else proposal_id
        logger.info(f"Buying contract with proposal ID: {id_preview}... at price: {price}")
        
        # Send the buy request using the official API
        response = await api.buy(buy_request)
        
        # Check for errors
        if response and 'error' in response:
            error_details = response.get('error', {})
            logger.error(f"Contract purchase failed: {error_details}")
            return None
        
        # Log successful purchase
        if response and 'buy' in response:
            contract_info = response.get('buy')
            logger.info(f"Contract purchased successfully - Contract ID: {contract_info.get('contract_id')}, "
                       f"Purchase Time: {contract_info.get('purchase_time')}, "
                       f"Balance After: {contract_info.get('balance_after')}")
        
        return response
        
    except Exception as e:
        id_preview = proposal_id[:8] if len(proposal_id) > 8 else proposal_id
        logger.exception(f"Error buying option contract with proposal ID {id_preview}...: {e}")
        return None

async def subscribe_to_contract_updates(api_wrapper, contract_id, on_update_callback):
    """
    Subscribe to real-time updates for a specific contract.
    
    Parameters:
        api_wrapper: Connected DerivAPIWrapper object.
        contract_id (str/int): The ID of the contract to monitor.
        on_update_callback (callable): Function to handle update messages.
        
    Returns:
        dict: The subscription object with observable and disposable, or None on error.
    """
    try:
        # Ensure we access the underlying API object
        api = api_wrapper.api
        if not api:
            logger.error("API not initialized. Call connect() first.")
            return None
            
        logger.info(f"Attempting to subscribe to contract updates for contract ID: {contract_id}")
        
        # Construct the subscription request
        request = {
            "proposal_open_contract": 1,
            "contract_id": contract_id,
            "subscribe": 1
        }
        
        # Subscribe using the official API which returns an Observable
        observable = await api.subscribe(request)
        
        if not observable:
            logger.error("Failed to create contract updates subscription")
            return None
            
        # Subscribe to the Observable with the callback
        disposable = observable.subscribe(on_update_callback)
        
        logger.info(f"Successfully initiated subscription for contract ID: {contract_id}")
        
        # Return both the observable and the disposable for later reference
        return {
            "observable": observable,
            "disposable": disposable
        }
        
    except Exception as e:
        logger.exception(f"Error subscribing to contract updates for contract ID: {contract_id}: {e}")
        return None