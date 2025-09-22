import pandas as pd
import numpy as np

def create_signal(prices_df):
    """
    Create investment signal based on average returns over the past year.
    
    Args:
        prices_df (pd.DataFrame): Preprocessed prices DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with signal column added
    """
    # Calculate 12-month rolling average of past returns
    prices_df['average_return_1y'] = prices_df.groupby('ticker')['monthly_past_return'].rolling(
        window=12, min_periods=1).mean().reset_index(0, drop=True)
    
    # Create signal: True for top 20 stocks each month
    def get_top_20_signal(group):
        if len(group) < 20:
            # If fewer than 20 stocks, select all
            group['signal'] = True
        else:
            # Select top 20 based on average_return_1y
            top_20_idx = group['average_return_1y'].nlargest(20).index
            group['signal'] = False
            group.loc[top_20_idx, 'signal'] = True
        return group
    
    # Apply signal creation for each date
    prices_df = prices_df.groupby('date').apply(get_top_20_signal)
    
    return prices_df