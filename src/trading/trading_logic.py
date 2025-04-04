import logging
import asyncio
from typing import Dict, Optional, Union, Any

# Configure logger
logger = logging.getLogger("DerivBot")

async def execute_trade(
    api: Any,
    signal: str,
    instrument: str,
    stake_amount: float,
    duration: int,
    duration_unit: str
) -> Optional[Dict]:
    """
    Execute a trade based on the provided signal.
    
    Args:
        api: The Deriv API client
        signal: Trading signal ("BUY" or "SELL")
        instrument: The trading instrument symbol
        stake_amount: Amount to stake on the trade
        duration: Duration of the contract
        duration_unit: Unit for duration ('m' for minutes, 'h' for hours, etc.)
        
    Returns:
        Dict containing the trade result or None if trade failed
    """
    try:
        logger.info(f"Executing {signal} trade for {instrument} with stake {stake_amount}")
        
        # Convert signal to contract type
        contract_type = "CALL" if signal == "BUY" else "PUT"
        
        # Get proposal for the option contract
        logger.debug(f"Requesting proposal for {contract_type} option")
        response = await api.proposal({
            "proposal": 1,
            "contract_type": contract_type,
            "currency": "USD",
            "symbol": instrument,
            "amount": stake_amount,
            "duration": duration,
            "duration_unit": duration_unit,
            "barrier": "+0.10",  # Example barrier, adjust as needed
            "basis": "stake"
        })
        
        if "error" in response:
            logger.error(f"Proposal error: {response['error']['message']}")
            return None
            
        if "proposal" not in response:
            logger.error("Unexpected response format - no proposal found")
            return None
            
        proposal_id = response["proposal"]["id"]
        ask_price = response["proposal"]["ask_price"]
        
        logger.info(f"Buying contract with proposal ID: {proposal_id}, price: {ask_price}")
        
        # Buy the contract
        buy_response = await api.buy({
            "buy": proposal_id,
            "price": ask_price
        })
        
        if "error" in buy_response:
            logger.error(f"Buy error: {buy_response['error']['message']}")
            return None
            
        logger.info(f"Trade executed successfully: {buy_response['buy']['contract_id']}")
        return buy_response
        
    except Exception as e:
        logger.error(f"Error executing trade: {str(e)}")
        return None


def validate_signal(
    signal: str,
    current_price: float,
    account_balance: float,
    active_positions: int,
    max_positions: int
) -> bool:
    """
    Validate if a trading signal should be acted upon.
    
    Args:
        signal: Trading signal ("BUY" or "SELL")
        current_price: Current price of the instrument
        account_balance: Available account balance
        active_positions: Number of currently active positions
        max_positions: Maximum allowed concurrent positions
        
    Returns:
        Bool indicating whether the signal is valid
    """
    # Check if signal is valid
    if signal not in ["BUY", "SELL"]:
        logger.warning(f"Invalid signal: {signal}")
        return False
        
    # Check if we have reached max positions
    if active_positions >= max_positions:
        logger.info(f"Max positions reached. Active: {active_positions}, Max: {max_positions}")
        return False
        
    # Basic check for sufficient balance
    # Assuming we need at least the current price to execute a trade
    if account_balance < current_price:
        logger.info(f"Insufficient balance: {account_balance} < {current_price}")
        return False
        
    return True


def calculate_position_size(
    account_balance: float,
    risk_per_trade: float,
    current_price: float,
    stop_loss_pct: float,
    max_position_pct: float = 0.1  # Default to 10% maximum position size
) -> float:
    """
    Calculate the position size based on risk parameters.
    
    Args:
        account_balance: Available account balance
        risk_per_trade: Percentage of account to risk per trade (0.02 = 2%)
        current_price: Current price of the instrument
        stop_loss_pct: Percentage for stop loss placement (0.02 = 2%)
        max_position_pct: Maximum percentage of account balance for a single position
        
    Returns:
        Float representing the position size
    """
    if account_balance <= 0 or current_price <= 0 or stop_loss_pct <= 0:
        return 0.0
        
    # Calculate risk amount
    risk_amount = account_balance * risk_per_trade
    
    # Calculate position size based on risk amount and stop loss percentage
    # Risk per pip = Risk amount / (stop loss in pips)
    position_size = risk_amount / stop_loss_pct
    
    # Apply maximum position size as percentage of account balance
    max_allowed_position = account_balance * max_position_pct
    position_size = min(position_size, max_allowed_position)
    
    logger.debug(f"Calculated position size: {position_size} (max allowed: {max_allowed_position})")
    return position_size