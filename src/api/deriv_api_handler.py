import asyncio
import json
import websockets
from config.settings import API_TOKEN, APP_ID
from src.utils.logger import setup_logger

# Set up logger globally
logger = setup_logger()

# Create a wrapper class for Deriv API with async functionality using WebSockets
class DerivAPIAsync:
    def __init__(self, api_key):
        self.api_key = api_key
        self.app_id = APP_ID
        self.ws = None
        self.connected = False
        self.request_id = 1
        self.pending_requests = {}
        self.subscriptions = {}
        self.websocket_url = "wss://ws.binaryws.com/websockets/v3"
        
    async def connect(self):
        """Connect to Deriv API via WebSocket."""
        if self.connected and self.ws:
            logger.debug("Already connected to Deriv API")
            return True
            
        try:
            self.ws = await websockets.connect(self.websocket_url)
            self.connected = True
            
            # Start listening for messages in a separate task
            asyncio.create_task(self._listen_messages())
            
            # Authorize with API key
            auth_response = await self._send_request({
                "authorize": self.api_key,
                "app_id": self.app_id
            })
            
            if auth_response and not auth_response.get('error'):
                logger.info("Successfully connected and authorized with Deriv API")
                return True
            else:
                error_msg = auth_response.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Authorization failed: {error_msg}")
                await self.disconnect()
                return False
                
        except Exception as e:
            logger.exception(f"Failed to connect to Deriv API: {e}")
            self.ws = None
            self.connected = False
            return False
            
    async def _listen_messages(self):
        """Listen for incoming messages on the WebSocket connection."""
        try:
            while self.connected and self.ws:
                try:
                    message = await self.ws.recv()
                    message_json = json.loads(message)
                    req_id = message_json.get('req_id')
                    
                    # Handle pending requests
                    if req_id and req_id in self.pending_requests:
                        self.pending_requests[req_id].set_result(message_json)
                    
                    # Handle subscriptions
                    msg_type = message_json.get('msg_type')
                    if msg_type in self.subscriptions:
                        for callback in self.subscriptions.get(msg_type, []):
                            asyncio.create_task(callback(message_json))
                            
                except websockets.exceptions.ConnectionClosed:
                    logger.warning("WebSocket connection closed unexpectedly")
                    self.connected = False
                    break
                except Exception as e:
                    logger.exception(f"Error processing message: {e}")
        except Exception as e:
            logger.exception(f"Error in message listener: {e}")
        finally:
            self.connected = False
            
    async def _send_request(self, request_data):
        """Send a request to the Deriv API and wait for a response."""
        if not self.connected:
            success = await self.connect()
            if not success:
                return {"error": {"message": "Failed to connect to API"}}
                
        req_id = self.request_id
        self.request_id += 1
        
        request_data['req_id'] = req_id
        future = asyncio.Future()
        self.pending_requests[req_id] = future
        
        try:
            await self.ws.send(json.dumps(request_data))
            response = await asyncio.wait_for(future, timeout=30)
            return response
        except asyncio.TimeoutError:
            logger.error(f"Request timed out: {request_data}")
            return {"error": {"message": "Request timed out"}}
        except Exception as e:
            logger.exception(f"Error sending request: {e}")
            return {"error": {"message": str(e)}}
        finally:
            if req_id in self.pending_requests:
                del self.pending_requests[req_id]
            
    async def disconnect(self):
        """Disconnect from Deriv API."""
        if not self.connected or not self.ws:
            return True
            
        try:
            await self.ws.close()
            self.connected = False
            self.ws = None
            self.pending_requests = {}
            self.subscriptions = {}
            logger.info("Disconnected from Deriv API")
            return True
        except Exception as e:
            logger.exception(f"Error disconnecting from Deriv API: {e}")
            return False
            
    async def proposal(self, request):
        """Get a proposal from the API."""
        return await self._send_request(request)
        
    async def buy(self, request):
        """Buy a contract."""
        return await self._send_request(request)
        
    async def subscribe(self, request):
        """Subscribe to updates."""
        response = await self._send_request(request)
        
        # For tick subscription, set up a subscription handler
        if 'ticks' in request:
            symbol = request['ticks']
            msg_type = 'tick'
            if msg_type not in self.subscriptions:
                self.subscriptions[msg_type] = []
                
        return response
        
    async def add_subscription_handler(self, msg_type, callback):
        """Add a callback handler for a specific message type."""
        if msg_type not in self.subscriptions:
            self.subscriptions[msg_type] = []
        self.subscriptions[msg_type].append(callback)
        
    async def balance(self):
        """Get account balance."""
        return await self._send_request({"balance": 1, "account": "all"})

# Define a default message handler
async def default_message_handler(message):
    """Handle incoming messages from the Deriv API."""
    # Log all incoming messages to see if ticks arrive here
    logger.debug(f"Default Handler Received Message: {message}")
    # Check if it's a tick message
    if message.get('msg_type') == 'tick':
        logger.info(f"Tick received via default handler: {message.get('tick')}")
    # Add handling for other message types if needed

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
        api: Connected DerivAPIAsync object.
        contract_id (str/int): The ID of the contract to monitor.
        on_update_callback (callable): Function to handle update messages.
        
    Returns:
        bool: True if subscription was successful, False otherwise.
    """
    try:
        logger.info(f"Attempting to subscribe to contract updates for contract ID: {contract_id}")
        
        # Construct the subscription request
        request = {
            "proposal_open_contract": 1,
            "contract_id": contract_id
        }
        
        # Subscribe and get the response
        response = await api.subscribe(request)
        
        if 'error' in response:
            logger.error(f"Contract subscription error: {response['error']['message']}")
            return False
            
        # Set up a message handler for contract updates
        subscription_msg_type = "proposal_open_contract"
        
        # Register the subscription handler
        await api.add_subscription_handler(
            subscription_msg_type, 
            on_update_callback
        )
        
        logger.info(f"Successfully initiated subscription for contract ID: {contract_id}")
        return True
        
    except Exception as e:
        logger.exception(f"Error subscribing to contract updates for contract ID: {contract_id}")
        return False