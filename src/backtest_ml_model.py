
#!/usr/bin/env python3
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.api.deriv_api_handler import connect_deriv_api, disconnect
from src.data.data_handler import get_historical_data
from src.utils.backtest import SimpleBacktester
from src.utils.logger import setup_logger
from src.models.signal_model import (
    train_or_load_model,
    engineer_features,
    generate_signals_for_dataset,
    FEATURE_COLUMNS
)
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT

# Set up logger
logger = setup_logger()

async def run_ml_backtest():
    """Run a backtest using RandomForest model with historical data."""
    logger.info("Starting RandomForest model backtest...")
    
    # Connect to API and get historical data
    api = await connect_deriv_api()
    if not api:
        logger.error("Failed to connect to API. Cannot proceed with backtest.")
        return
        
    try:
        # Fetch a larger dataset for meaningful backtest
        backtest_bars = max(1000, HISTORICAL_BARS_COUNT * 2)
        historical_df = await get_historical_data(api, INSTRUMENT, TIMEFRAME_SECONDS, backtest_bars)
        
        if historical_df.empty:
            logger.error("Failed to fetch historical data for backtest.")
            return
            
        logger.info(f"Successfully fetched {len(historical_df)} historical data points for RandomForest backtest.")
        
        # Load trained model and scaler
        model, scaler = train_or_load_model()
        
        if model is None:
            logger.error("Failed to load RandomForest model. Cannot proceed with backtest.")
            return
            
        # Engineer features using enhanced feature set
        logger.info("Engineering features with enhanced indicators...")
        feature_df = engineer_features(historical_df.copy())
        
        if len(feature_df) == 0:
            logger.error("Feature engineering resulted in empty dataset. Cannot proceed.")
            return
        
        # Log sample data and verify feature columns
        logger.info("Feature data sample:")
        logger.info(feature_df[FEATURE_COLUMNS].head())
        
        # Log null values to check data quality
        logger.info("Null values in features:")
        logger.info(feature_df[FEATURE_COLUMNS].isnull().sum())
            
        logger.info(f"Feature engineering generated {len(feature_df)} samples with {len(FEATURE_COLUMNS)} features.")
        
        # Generate ML signals for the entire dataset
        logger.info("Generating RandomForest signals for the entire dataset...")
        signals = generate_signals_for_dataset(model, scaler, historical_df)
        
        if len(signals) == 0:
            logger.error("No signals generated. Cannot proceed with backtest.")
            return
            
        # Initialize backtester
        initial_capital = 1000
        backtester = SimpleBacktester(initial_capital=initial_capital)
        
        # Run backtest with ML signals
        backtest_results = backtester.run_backtest(
            historical_df=feature_df,
            signals=signals,
            risk_per_trade=0.02,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            max_position_size=0.25,
            leverage=1
        )
        
        if backtest_results:
            metrics = backtest_results['metrics']
            trades_df = backtest_results['trades']
            equity_curve = backtest_results['equity_curve']
            
            logger.info("--- RandomForest Backtest Summary ---")
            logger.info(f"Initial Capital: ${metrics['initial_capital']:.2f}")
            logger.info(f"Final Capital: ${metrics['final_capital']:.2f}")
            logger.info(f"Total Return: {metrics['total_return_pct']:.2f}%")
            logger.info(f"Total Trades: {metrics['total_trades']}")
            logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
            
            if len(trades_df) > 0:
                trades_df.to_csv('random_forest_trades.csv')
                logger.info("Saved trade history to random_forest_trades.csv")
                
                try:
                    plt.figure(figsize=(12, 6))
                    plt.plot(equity_curve['time'], equity_curve['capital'], label='Portfolio Value')
                    plt.title('RandomForest Trading Strategy Equity Curve')
                    plt.xlabel('Time')
                    plt.ylabel('Portfolio Value ($)')
                    plt.grid(True, alpha=0.3)
                    plt.legend()
                    plt.tight_layout()
                    plt.savefig('random_forest_equity_curve.png')
                    logger.info("Saved RandomForest equity curve plot to random_forest_equity_curve.png")
                except Exception as e:
                    logger.warning(f"Could not create equity curve plot: {e}")
        else:
            logger.warning("RandomForest backtest did not return any results.")
    
    except Exception as e:
        logger.exception(f"Error during RandomForest backtesting: {e}")
    
    finally:
        await disconnect(api)
        logger.info("RandomForest Backtest completed.")

if __name__ == "__main__":
    asyncio.run(run_ml_backtest())
