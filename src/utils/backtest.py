import pandas as pd
import numpy as np
from src.models.signal_model import SHORT_MA_PERIOD, LONG_MA_PERIOD
from src.utils.logger import setup_logger

logger = setup_logger()

class SimpleBacktester:
    """
    A simple backtester for evaluating trading strategies against historical data.
    """
    
    def __init__(self, initial_capital=1000.0):
        """
        Initialize the backtester.
        
        Parameters:
            initial_capital (float): The starting capital for the backtest.
        """
        self.initial_capital = initial_capital
    
    def run_backtest(self, historical_df, signals=None, short_period=SHORT_MA_PERIOD, long_period=LONG_MA_PERIOD, 
                    risk_per_trade=0.02, stop_loss_pct=0.01, take_profit_pct=0.02, 
                    max_position_size=None, leverage=1):
        """
        Run a backtest of a trading strategy.
        
        Parameters:
            historical_df (pd.DataFrame): Historical price data with 'time' and 'close' columns.
            signals (pd.Series, optional): Pre-calculated signals (1=buy, -1=sell, 0=hold).
                                          If None, SMA crossover signals will be calculated.
            short_period (int): Period for the short SMA (only used if signals=None).
            long_period (int): Period for the long SMA (only used if signals=None).
            risk_per_trade (float): Percentage of capital to risk per trade (0.02 = 2%).
            stop_loss_pct (float): Stop loss percentage (0.01 = 1%).
            take_profit_pct (float): Take profit percentage (0.02 = 2%).
            max_position_size (float): Maximum position size as percentage of capital (e.g., 0.25 = 25%).
            leverage (float): Trading leverage (1 = no leverage, 2 = 2x leverage, etc.)
            
        Returns:
            pd.DataFrame: Results of the backtest with performance metrics.
        """
        # Ensure we have the required columns
        if 'close' not in historical_df.columns:
            logger.error("Historical data missing 'close' column for backtest")
            return None
        
        # Make a copy to avoid modifying original data
        df = historical_df.copy()
        
        calculate_sma_signals = True

        # If external signals are provided, use them instead of calculating SMA signals
        if signals is not None:
            logger.info("Using provided external signals for backtest.")
            # Ensure index alignment if necessary before assigning
            if df.index.equals(signals.index):
                df['signal'] = signals
                calculate_sma_signals = False
            else:
                logger.warning("External signals index does not match DataFrame index. Attempting reindex.")
                # Try to align, handle potential errors if alignment fails
                try:
                    df['signal'] = signals.reindex(df.index).fillna(0)
                    calculate_sma_signals = False
                except Exception as e:
                    logger.error(f"Failed to align external signals: {e}. Proceeding with SMA calculation.")
                    calculate_sma_signals = True
        
        # Calculate SMA signals if external signals weren't provided or failed to align
        if calculate_sma_signals:
            logger.info("Calculating SMA signals for backtest.")
            # Calculate SMAs
            df['short_ma'] = df['close'].rolling(window=short_period).mean()
            df['long_ma'] = df['close'].rolling(window=long_period).mean()
            
            # Drop rows with NaN values from SMA calculations
            df = df.dropna().reset_index(drop=True)
            
            # Generate signals
            df['signal'] = 0  # 0: no signal, 1: buy, -1: sell
            
            # Buy signal when short MA crosses above long MA
            df.loc[(df['short_ma'] > df['long_ma']) & (df['short_ma'].shift(1) <= df['long_ma'].shift(1)), 'signal'] = 1
            
            # Sell signal when short MA crosses below long MA
            df.loc[(df['short_ma'] < df['long_ma']) & (df['short_ma'].shift(1) >= df['long_ma'].shift(1)), 'signal'] = -1
        
        # Initialize position, capital, and trade tracking
        # Fix for FutureWarning: replace deprecated 'method' parameter with modern methods
        df['position'] = df['signal'].copy()
        df['position'] = df['position'].replace(to_replace=0, value=np.nan)
        df['position'] = df['position'].ffill()  # Use ffill() instead of fillna(method='ffill')
        df['position'] = df['position'].fillna(0)
        
        # Capital tracking
        df['capital'] = self.initial_capital
        df['trade_active'] = False
        df['trade_entry'] = np.nan
        df['trade_exit'] = np.nan
        df['trade_pnl'] = 0.0
        
        # Run simulation
        capital = self.initial_capital
        position = 0
        trade_active = False
        entry_price = 0
        stop_loss = 0
        take_profit = 0
        shares = 0
        
        trades = []
        
        for i in range(1, len(df)):
            current_price = df.iloc[i]['close']
            current_signal = df.iloc[i]['signal']
            prev_position = position
            
            # Check if we need to exit due to SL/TP
            if trade_active:
                # For long positions
                if position == 1:
                    if current_price <= stop_loss:  # Stop loss hit
                        position = 0
                        trade_result = shares * (stop_loss - entry_price) * leverage
                        capital += shares * entry_price + trade_result  # Return initial capital + profit/loss
                        trades.append({
                            'entry_time': df.iloc[i-1]['time'],
                            'exit_time': df.iloc[i]['time'],
                            'entry_price': entry_price,
                            'exit_price': stop_loss,
                            'position': 'LONG',
                            'exit_type': 'STOP_LOSS',
                            'shares': shares,
                            'pnl': trade_result,
                            'pnl_pct': (trade_result/(shares * entry_price))*100
                        })
                        trade_active = False
                    elif current_price >= take_profit:  # Take profit hit
                        position = 0
                        trade_result = shares * (take_profit - entry_price) * leverage
                        capital += shares * entry_price + trade_result  # Return initial capital + profit
                        trades.append({
                            'entry_time': df.iloc[i-1]['time'],
                            'exit_time': df.iloc[i]['time'],
                            'entry_price': entry_price,
                            'exit_price': take_profit,
                            'position': 'LONG',
                            'exit_type': 'TAKE_PROFIT',
                            'shares': shares,
                            'pnl': trade_result,
                            'pnl_pct': (trade_result/(shares * entry_price))*100
                        })
                        trade_active = False
                # For short positions
                elif position == -1:
                    if current_price >= stop_loss:  # Stop loss hit
                        position = 0
                        trade_result = shares * (entry_price - stop_loss) * leverage
                        capital += shares * entry_price + trade_result  # Return margin + profit/loss
                        trades.append({
                            'entry_time': df.iloc[i-1]['time'],
                            'exit_time': df.iloc[i]['time'],
                            'entry_price': entry_price,
                            'exit_price': stop_loss,
                            'position': 'SHORT',
                            'exit_type': 'STOP_LOSS',
                            'shares': shares,
                            'pnl': trade_result,
                            'pnl_pct': (trade_result/(shares * entry_price))*100
                        })
                        trade_active = False
                    elif current_price <= take_profit:  # Take profit hit
                        position = 0
                        trade_result = shares * (entry_price - take_profit) * leverage
                        capital += shares * entry_price + trade_result  # Return margin + profit
                        trades.append({
                            'entry_time': df.iloc[i-1]['time'],
                            'exit_time': df.iloc[i]['time'],
                            'entry_price': entry_price,
                            'exit_price': take_profit,
                            'position': 'SHORT',
                            'exit_type': 'TAKE_PROFIT',
                            'shares': shares,
                            'pnl': trade_result,
                            'pnl_pct': (trade_result/(shares * entry_price))*100
                        })
                        trade_active = False
            
            # Check for new signal
            if current_signal != 0 and not trade_active:
                # Close any existing position (not needed for this simple backtest, but good practice)
                if position != 0:
                    position = 0
                    
                # Enter new position
                position = current_signal
                entry_price = current_price
                risk_amount = capital * risk_per_trade
                
                # Calculate position size based on risk
                if position == 1:  # Long position
                    stop_loss = entry_price * (1 - stop_loss_pct)
                    take_profit = entry_price * (1 + take_profit_pct)
                    
                    # Calculate position size while accounting for leverage
                    price_distance = entry_price - stop_loss
                    shares = risk_amount / (price_distance * leverage)
                    
                    # Apply maximum position size constraint if specified
                    if max_position_size:
                        max_shares = (capital * max_position_size) / entry_price
                        shares = min(shares, max_shares)
                    
                    # Subtract cost of shares from capital (adjusted for leverage)
                    position_cost = (shares * entry_price) / leverage
                    capital -= position_cost
                    
                else:  # Short position
                    stop_loss = entry_price * (1 + stop_loss_pct)
                    take_profit = entry_price * (1 - take_profit_pct)
                    
                    # Calculate position size while accounting for leverage
                    price_distance = stop_loss - entry_price
                    shares = risk_amount / (price_distance * leverage)
                    
                    # Apply maximum position size constraint if specified
                    if max_position_size:
                        max_shares = (capital * max_position_size) / entry_price
                        shares = min(shares, max_shares)
                    
                    # Subtract margin requirement from capital (adjusted for leverage)
                    position_cost = (shares * entry_price) / leverage
                    capital -= position_cost
                
                trade_active = True
                
                # Log trade entry
                logger.debug(f"Entering {position} position at {entry_price}, shares: {shares}, SL: {stop_loss}, TP: {take_profit}")
            
            # Update tracking data
            df.at[i, 'position'] = position
            df.at[i, 'capital'] = float(capital)
            df.at[i, 'trade_active'] = trade_active
            
            if trade_active:
                df.at[i, 'trade_entry'] = entry_price
                
                # Calculate current unrealized P&L
                if position == 1:  # Long position
                    df.at[i, 'trade_pnl'] = shares * (current_price - entry_price)
                elif position == -1:  # Short position
                    df.at[i, 'trade_pnl'] = shares * (entry_price - current_price)
        
        # Generate performance metrics
        if trades:
            trades_df = pd.DataFrame(trades)
            
            # Calculate metrics
            total_trades = len(trades_df)
            winning_trades = len(trades_df[trades_df['pnl'] > 0])
            losing_trades = total_trades - winning_trades
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
            avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
            
            final_capital = capital
            for pnl in trades_df['pnl']:
                if position == 1:  # For active long position
                    final_capital += pnl
            
            total_return = ((final_capital - self.initial_capital) / self.initial_capital) * 100
            
            # Add metrics to the results
            metrics = {
                'initial_capital': self.initial_capital,
                'final_capital': final_capital,
                'total_return_pct': total_return,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': win_rate,
                'avg_win': avg_win,
                'avg_loss': avg_loss
            }
            
            logger.info(f"Backtest Results: {metrics}")
            
            return {
                'metrics': metrics,
                'trades': trades_df,
                'equity_curve': df[['time', 'close', 'capital', 'position', 'trade_pnl']]
            }
        else:
            logger.warning("No trades executed during backtest period")
            return {
                'metrics': {
                    'initial_capital': self.initial_capital,
                    'final_capital': capital,
                    'total_return_pct': 0,
                    'total_trades': 0
                },
                'trades': pd.DataFrame(),
                'equity_curve': df[['time', 'close', 'capital', 'position', 'trade_pnl']]
            }