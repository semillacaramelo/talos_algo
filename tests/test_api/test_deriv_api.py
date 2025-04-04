import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.api.deriv_api_handler import connect_deriv_api, disconnect, get_option_proposal, buy_option_contract

@pytest.mark.api
@pytest.mark.unit
class TestDerivAPIHandler:
    
    @pytest.mark.asyncio
    async def test_connect_deriv_api(self, mock_api):
        """Test API connection establishment."""
        with patch('src.api.deriv_api_handler.DerivAPI', return_value=mock_api):
            api = await connect_deriv_api()
            assert api is not None
            mock_api.authorize.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_api(self, mock_api):
        """Test API disconnection."""
        result = await disconnect(mock_api)
        assert result is True
        mock_api.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_option_proposal(self, mock_api):
        """Test option proposal request."""
        # Setup mock response
        mock_api.proposal = AsyncMock(return_value={
            'proposal': {
                'id': 'test_proposal',
                'ask_price': 10.0,
                'payout': 20.0
            }
        })

        result = await get_option_proposal(
            mock_api, 'R_100', 'CALL', 1, 'm', 'USD', 1.0, 'stake'
        )
        assert result is not None
        assert 'proposal' in result
        assert result['proposal']['id'] == 'test_proposal'

    @pytest.mark.asyncio
    async def test_buy_option_contract(self, mock_api):
        """Test option contract purchase."""
        # Setup mock response
        mock_api.buy = AsyncMock(return_value={
            'buy': {
                'contract_id': 'test_contract',
                'purchase_time': 1234567890,
                'balance_after': 990.0
            }
        })

        result = await buy_option_contract(mock_api, 'test_proposal', 10.0)
        assert result is not None
        assert 'buy' in result
        assert result['buy']['contract_id'] == 'test_contract'

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, mock_api):
        """Test error handling during connection."""
        mock_api.authorize.side_effect = Exception("Connection failed")
        
        with patch('src.api.deriv_api_handler.DerivAPI', return_value=mock_api):
            api = await connect_deriv_api()
            assert api is None

    @pytest.mark.asyncio
    async def test_proposal_error_handling(self, mock_api):
        """Test error handling for proposal requests."""
        mock_api.proposal = AsyncMock(return_value={
            'error': {
                'code': 'InvalidAmount',
                'message': 'Invalid amount'
            }
        })

        result = await get_option_proposal(
            mock_api, 'R_100', 'CALL', 1, 'm', 'USD', -1.0, 'stake'
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_buy_error_handling(self, mock_api):
        """Test error handling for buy requests."""
        mock_api.buy = AsyncMock(side_effect=Exception("Purchase failed"))

        result = await buy_option_contract(mock_api, 'test_proposal', 10.0)
        assert result is None

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_api_integration(self, mock_api):
        """Test complete API flow with integration test."""
        with patch('src.api.deriv_api_handler.DerivAPI', return_value=mock_api):
            # Connect
            api = await connect_deriv_api()
            assert api is not None

            # Get proposal
            mock_api.proposal = AsyncMock(return_value={
                'proposal': {
                    'id': 'test_proposal',
                    'ask_price': 10.0,
                    'payout': 20.0
                }
            })
            
            proposal = await get_option_proposal(
                api, 'R_100', 'CALL', 1, 'm', 'USD', 1.0, 'stake'
            )
            assert proposal is not None

            # Buy contract
            mock_api.buy = AsyncMock(return_value={
                'buy': {
                    'contract_id': 'test_contract',
                    'purchase_time': 1234567890,
                    'balance_after': 990.0
                }
            })
            
            purchase = await buy_option_contract(
                api, proposal['proposal']['id'], proposal['proposal']['ask_price']
            )
            assert purchase is not None

            # Disconnect
            result = await disconnect(api)
            assert result is True