import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from src.api.deriv_api_handler import connect_deriv_api, disconnect
from src.data.data_handler import get_historical_data
from src.utils.backtest import SimpleBacktester
from src.utils.logger import setup_logger
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT
from src.models.signal_model import SHORT_MA_PERIOD, LONG_MA_PERIOD

# Set up logger
logger = setup_logger()

async def run_backtest():
    """
    Run a backtest of our SMA crossover strategy with historical data from Deriv API.
    """
    logger.info("Starting strategy backtest...")
    
    # Connect to API and get historical data
    api = await connect_deriv_api()
    if not api:
        logger.error("Failed to connect to API. Cannot proceed with backtest.")
        return
        
    try:
        # Fetch a larger dataset for meaningful backtest
        backtest_bars = max(500, HISTORICAL_BARS_COUNT)  # Use at least 500 bars for backtest
        historical_df = await get_historical_data(api, INSTRUMENT, TIMEFRAME_SECONDS, backtest_bars)
        
        if historical_df.empty:
            logger.error("Failed to fetch historical data for backtest.")
            return
            
        logger.info(f"Successfully fetched {len(historical_df)} historical data points for backtest.")
        
        # Initialize backtester
        initial_capital = 1000  # Starting with $1000
        backtester = SimpleBacktester(initial_capital=initial_capital)
        
        # Run backtest
        backtest_results = backtester.run_sma_backtest(
            historical_df=historical_df,
            short_period=SHORT_MA_PERIOD,
            long_period=LONG_MA_PERIOD,
            risk_per_trade=0.02,      # Risk 2% per trade
            stop_loss_pct=0.01,       # 1% stop loss
            take_profit_pct=0.02,     # 2% take profit
            max_position_size=0.25,   # Maximum 25% of capital in any trade
            leverage=1                # No leverage (1x) for safer backtesting
        )
        
        if backtest_results:
            # Display results
            metrics = backtest_results['metrics']
            trades_df = backtest_results['trades']
            equity_curve = backtest_results['equity_curve']
            
            logger.info("Backtest Summary:")
            logger.info(f"Initial Capital: ${metrics['initial_capital']:.2f}")
            logger.info(f"Final Capital: ${metrics['final_capital']:.2f}")
            logger.info(f"Total Return: {metrics['total_return_pct']:.2f}%")
            logger.info(f"Total Trades: {metrics['total_trades']}")
            
            if metrics['total_trades'] > 0:
                logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
                logger.info(f"Avg Win: ${metrics['avg_win']:.2f}")
                logger.info(f"Avg Loss: ${metrics['avg_loss']:.2f}")
                
                # Save trades to CSV
                if not trades_df.empty:
                    trades_df.to_csv("backtest_trades.csv", index=False)
                    logger.info("Saved trades to backtest_trades.csv")
                
                # Save backtest results
                equity_curve.to_csv("backtest_equity_curve.csv", index=False)
                logger.info("Saved equity curve to backtest_equity_curve.csv")
                
                # Create and save a simple equity curve plot (if matplotlib is available)
                try:
                    plt.figure(figsize=(12, 6))
                    plt.plot(equity_curve['time'], equity_curve['capital'], label='Equity Curve')
                    plt.title(f'SMA Crossover Strategy Backtest - {INSTRUMENT}')
                    plt.xlabel('Time')
                    plt.ylabel('Capital ($)')
                    plt.legend()
                    plt.tight_layout()
                    plt.savefig('backtest_equity_curve.png')
                    logger.info("Saved equity curve plot to backtest_equity_curve.png")
                except Exception as e:
                    logger.warning(f"Could not create equity curve plot: {e}")
        else:
            logger.warning("Backtest did not return any results.")
    
    finally:
        # Disconnect from API
        await disconnect(api)
        logger.info("Backtest completed.")

if __name__ == "__main__":
    asyncio.run(run_backtest())