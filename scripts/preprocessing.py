import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def preprocess_prices(prices_df, plot=False):
    """
    Preprocess stock prices data.
    
    Args:
        prices_df (pd.DataFrame): Raw prices DataFrame
        plot (bool): Whether to generate plots
        
    Returns:
        pd.DataFrame: Preprocessed prices DataFrame
    """
    # Convert date column to datetime and set as index
    prices_df['date'] = pd.to_datetime(prices_df['date'])
    prices_df = prices_df.set_index(['date', 'ticker'])
    
    # Resample to monthly and keep last value
    prices_monthly = prices_df.groupby('ticker').resample('ME', level=0).last()
    prices_monthly = prices_monthly.reset_index().set_index(['date', 'ticker'])
    
    # Filter price outliers (0.1$ to 10k$)
    prices_monthly = prices_monthly[(prices_monthly['price'] >= 0.1) & 
                                   (prices_monthly['price'] <= 10000)]
    
    # Calculate monthly returns
    prices_monthly = prices_monthly.sort_index()
    
    # Historical returns (past)
    prices_monthly['monthly_past_return'] = prices_monthly.groupby('ticker')['price'].pct_change()
    
    # Future returns
    prices_monthly['monthly_future_return'] = prices_monthly.groupby('ticker')['price'].pct_change().shift(-1)
    
    # Handle return outliers (exclude 2008-2009)
    for ticker in prices_monthly.index.get_level_values(1).unique():
        ticker_data = prices_monthly.loc[prices_monthly.index.get_level_values(1) == ticker]
        
        # Create crisis period mask for this ticker's data
        ticker_dates = ticker_data.index.get_level_values(0)
        crisis_mask = (ticker_dates >= '2008-01-01') & (ticker_dates <= '2009-12-31')
        non_crisis_data = ticker_data[~crisis_mask]
        
        # Replace outliers in past returns (only in non-crisis data)
        if len(non_crisis_data) > 0:
            outliers_past = (non_crisis_data['monthly_past_return'] > 1) | \
                           (non_crisis_data['monthly_past_return'] < -0.5)
            if outliers_past.any():
                outlier_indices = non_crisis_data[outliers_past].index
                prices_monthly.loc[outlier_indices, 'monthly_past_return'] = np.nan
        
        # Replace outliers in future returns (only in non-crisis data)
        if len(non_crisis_data) > 0:
            outliers_future = (non_crisis_data['monthly_future_return'] > 1) | \
                             (non_crisis_data['monthly_future_return'] < -0.5)
            if outliers_future.any():
                outlier_indices = non_crisis_data[outliers_future].index
                prices_monthly.loc[outlier_indices, 'monthly_future_return'] = np.nan
    
    # Fill missing values with forward fill (except future returns)
    prices_monthly['price'] = prices_monthly.groupby('ticker')['price'].ffill()
    prices_monthly['monthly_past_return'] = prices_monthly.groupby('ticker')['monthly_past_return'].ffill()
    
    # Don't fill future returns - drop rows where future return is missing
    prices_monthly = prices_monthly.dropna(subset=['monthly_future_return'])
    
    # Drop any remaining missing values
    prices_monthly = prices_monthly.dropna()
    
    if plot:
        plot_price_analysis(prices_monthly)
    
    return prices_monthly

def preprocess_sp500(sp500_df):
    """
    Preprocess S&P 500 data.
    
    Args:
        sp500_df (pd.DataFrame): Raw S&P 500 DataFrame
        
    Returns:
        pd.DataFrame: Preprocessed S&P 500 DataFrame
    """
    # Convert date to datetime
    sp500_df['date'] = pd.to_datetime(sp500_df['date'])
    sp500_df = sp500_df.set_index('date')
    
    # Resample to monthly and keep last value
    sp500_monthly = sp500_df.resample('ME').last()
    
    # Calculate historical monthly returns
    sp500_monthly['monthly_return'] = sp500_monthly['adj_close'].pct_change()
    
    return sp500_monthly

def plot_price_analysis(prices_df, plot=False):
    """
    Generate price analysis plots.
    
    Args:
        prices_df (pd.DataFrame): Processed prices DataFrame
        plot (bool): Whether to save plots
    """
    if not plot:
        return
        
    # Average price over time
    avg_prices = prices_df.groupby('date')['price'].mean()
    
    plt.figure(figsize=(12, 6))
    plt.plot(avg_prices.index, avg_prices.values)
    plt.title('Average Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Price ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    os.makedirs('../results/plots', exist_ok=True)
    plt.savefig('../results/plots/average_price_over_time.png')
    plt.close()

def identify_outliers(prices_df):
    """
    Identify and save outliers to file.
    
    Args:
        prices_df (pd.DataFrame): Prices DataFrame
    """
    outliers = []
    
    for ticker in prices_df.index.get_level_values(1).unique():
        ticker_data = prices_df.loc[prices_df.index.get_level_values(1) == ticker]
        
        # Price outliers
        q1 = ticker_data['price'].quantile(0.25)
        q3 = ticker_data['price'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        price_outliers = ticker_data[(ticker_data['price'] < lower_bound) | 
                                    (ticker_data['price'] > upper_bound)]
        
        for idx, row in price_outliers.head(5).iterrows():
            date_str = idx[0].strftime('%Y-%m-%d') if hasattr(idx[0], 'strftime') else str(idx[0])
            outliers.append(f"{idx[1]},{date_str},{row['price']:.4f}")
    
    # Save outliers to file
    os.makedirs('../results', exist_ok=True)
    with open('../results/outliers.txt', 'w') as f:
        f.write("ticker,date,price\n")
        for outlier in outliers[:5]:
            f.write(outlier + "\n")

def preprocessing(prices_df, sp500_df, plot=False):
    """
    Main preprocessing function.
    
    Args:
        prices_df (pd.DataFrame): Raw prices DataFrame
        sp500_df (pd.DataFrame): Raw S&P 500 DataFrame
        plot (bool): Whether to generate plots
        
    Returns:
        tuple: Preprocessed prices and S&P 500 DataFrames
    """
    # Identify outliers before preprocessing
    identify_outliers(prices_df.set_index(['date', 'ticker']) if 'date' in prices_df.columns else prices_df)
    
    # Preprocess data
    prices_processed = preprocess_prices(prices_df, plot)
    sp500_processed = preprocess_sp500(sp500_df)
    
    print("Missing values after preprocessing:")
    print(prices_processed.isna().sum())
    
    return prices_processed, sp500_processed