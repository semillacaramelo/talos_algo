#!/usr/bin/env python3
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.api.deriv_api_handler import connect_deriv_api, disconnect
from src.data.data_handler import get_historical_data
from src.utils.backtest import SimpleBacktester
from src.utils.logger import setup_logger
from src.models.signal_model import train_or_load_model, engineer_features, generate_signals_for_dataset
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT

# Set up logger
logger = setup_logger()

async def run_ml_backtest():
    """
    Run a backtest using our trained ML model with historical data from Deriv API.
    """
    logger.info("Starting ML model backtest...")
    
    # Connect to API and get historical data
    api = await connect_deriv_api()
    if not api:
        logger.error("Failed to connect to API. Cannot proceed with backtest.")
        return
        
    try:
        # Fetch a larger dataset for meaningful backtest
        backtest_bars = max(1000, HISTORICAL_BARS_COUNT * 2)  # Use at least 1000 bars for ML backtest
        historical_df = await get_historical_data(api, INSTRUMENT, TIMEFRAME_SECONDS, backtest_bars)
        
        if historical_df.empty:
            logger.error("Failed to fetch historical data for backtest.")
            return
            
        logger.info(f"Successfully fetched {len(historical_df)} historical data points for ML backtest.")
        
        # Load trained model and scaler
        model, scaler = train_or_load_model()
        
        if model is None:
            logger.error("Failed to load ML model. Cannot proceed with ML backtest.")
            return
            
        # Engineer features for the entire historical dataset
        logger.info("Engineering features for ML backtesting...")
        feature_df = engineer_features(historical_df.copy())
        
        if len(feature_df) == 0:
            logger.error("Feature engineering resulted in empty dataset. Cannot proceed.")
            return
            
        logger.info(f"Feature engineering generated {len(feature_df)} samples with features.")
        
        # Generate ML signals for the entire dataset
        logger.info("Generating ML signals for the entire dataset...")
        signals = generate_signals_for_dataset(model, scaler, historical_df)
        
        if len(signals) == 0:
            logger.error("No signals generated. Cannot proceed with backtest.")
            return
            
        # Initialize backtester
        initial_capital = 1000  # Starting with $1000
        backtester = SimpleBacktester(initial_capital=initial_capital)
        
        # Run backtest with ML signals
        backtest_results = backtester.run_backtest(
            historical_df=feature_df,  # Use the feature-engineered dataframe with same indices
            signals=signals,           # Pass our ML-generated signals
            risk_per_trade=0.02,       # Risk 2% per trade
            stop_loss_pct=0.01,        # 1% stop loss
            take_profit_pct=0.02,      # 2% take profit
            max_position_size=0.25,    # Maximum 25% of capital in any trade
            leverage=1                 # No leverage (1x) for safer backtesting
        )
        
        if backtest_results:
            # Display results
            metrics = backtest_results['metrics']
            trades_df = backtest_results['trades']
            equity_curve = backtest_results['equity_curve']
            
            logger.info("--- Random Forest Backtest Summary ---")
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
                    trades_df.to_csv("ml_rf_backtest_trades.csv", index=False)
                    logger.info("Saved Random Forest trades to ml_rf_backtest_trades.csv")
                
                # Save backtest results
                equity_curve.to_csv("ml_rf_backtest_equity_curve.csv", index=False)
                logger.info("Saved Random Forest equity curve to ml_rf_backtest_equity_curve.csv")
                
                # Create and save a simple equity curve plot (if matplotlib is available)
                try:
                    plt.figure(figsize=(12, 6))
                    plt.plot(equity_curve['time'], equity_curve['capital'], label='Random Forest Equity Curve')
                    plt.title(f'Random Forest Strategy Backtest - {INSTRUMENT}')
                    plt.xlabel('Time')
                    plt.ylabel('Capital ($)')
                    plt.grid(True, alpha=0.3)
                    plt.legend()
                    plt.tight_layout()
                    plt.savefig('ml_rf_backtest_equity_curve.png')
                    logger.info("Saved Random Forest equity curve plot to ml_rf_backtest_equity_curve.png")
                except Exception as e:
                    logger.warning(f"Could not create equity curve plot: {e}")
        else:
            logger.warning("ML backtest did not return any results.")
    
    except Exception as e:
        logger.exception(f"Error during ML backtesting: {e}")
    
    finally:
        # Disconnect from API
        await disconnect(api)
        logger.info("ML Backtest completed.")

if __name__ == "__main__":
    asyncio.run(run_ml_backtest())
