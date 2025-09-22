import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def backtest(prices_df, sp500_df):
    """
    Backtest the stock picking strategy against S&P 500 benchmark.
    
    Args:
        prices_df (pd.DataFrame): Prices DataFrame with signals
        sp500_df (pd.DataFrame): S&P 500 DataFrame
    """
    # Calculate PnL by multiplying signal by future returns
    prices_df['pnl'] = prices_df['signal'] * prices_df['monthly_future_return']
    
    # Group by date and sum PnL
    strategy_pnl_series = prices_df.groupby('date')['pnl'].sum()
    
    # Calculate strategy returns by dividing PnL by sum of signals (number of stocks)
    signal_sum = prices_df.groupby('date')['signal'].sum()
    strategy_returns = strategy_pnl_series / signal_sum
    
    # S&P 500 benchmark with signal of 20 (investing $20)
    benchmark_returns = sp500_df['monthly_return'].dropna()
    sp500_signal = pd.Series([20] * len(benchmark_returns), index=benchmark_returns.index)
    benchmark_pnl_series = sp500_signal * benchmark_returns
    
    # Align dates
    common_dates = strategy_returns.index.intersection(benchmark_returns.index)
    strategy_returns = strategy_returns.loc[common_dates]
    strategy_pnl_series = strategy_pnl_series.loc[common_dates]
    benchmark_returns = benchmark_returns.loc[common_dates]
    benchmark_pnl_series = benchmark_pnl_series.loc[common_dates]
    
    # Calculate cumulative PnL for plotting
    strategy_cumulative_pnl = strategy_pnl_series.cumsum()
    benchmark_cumulative_pnl = benchmark_pnl_series.cumsum()
    
    # Calculate total returns
    strategy_total_return = strategy_returns.sum()
    benchmark_total_return = benchmark_returns.sum()
    
    # Calculate total PnL
    strategy_total_pnl = strategy_cumulative_pnl.iloc[-1]
    benchmark_total_pnl = benchmark_cumulative_pnl.iloc[-1]
    
    # Save results
    os.makedirs('../results', exist_ok=True)
    with open('../results/results.txt', 'w') as f:
        f.write("BACKTESTING RESULTS\n")
        f.write("==================\n\n")
        f.write("Stock Picking Strategy (Top 20):\n")
        f.write(f"Total Return: {strategy_total_return:.4f} ({strategy_total_return*100:.2f}%)\n")
        f.write(f"PnL: ${strategy_total_pnl:.2f}\n\n")
        f.write("S&P 500 Benchmark:\n")
        f.write(f"Total Return: {benchmark_total_return:.4f} ({benchmark_total_return*100:.2f}%)\n")
        f.write(f"PnL: ${benchmark_total_pnl:.2f}\n\n")
        f.write(f"Outperformance: {(strategy_total_return - benchmark_total_return)*100:.2f}%\n")
        f.write(f"Total PnL on full historical data: ${strategy_total_pnl:.2f}\n")
    
    # Create performance plot using cumulative PnL
    plt.figure(figsize=(12, 8))
    plt.plot(strategy_cumulative_pnl.index, strategy_cumulative_pnl.values, 
             label='Stock Picking Strategy (Top 20)', linewidth=2)
    plt.plot(benchmark_cumulative_pnl.index, benchmark_cumulative_pnl.values, 
             label='S&P 500 Benchmark', linewidth=2)
    
    plt.title('Strategy Performance vs S&P 500 Benchmark')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    os.makedirs('../results/plots', exist_ok=True)
    plt.savefig('../results/plots/strategy_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Strategy Total Return: {strategy_total_return:.4f} ({strategy_total_return*100:.2f}%)")
    print(f"Benchmark Total Return: {benchmark_total_return:.4f} ({benchmark_total_return*100:.2f}%)")
    print(f"Outperformance: {(strategy_total_return - benchmark_total_return)*100:.2f}%")
    print(f"Total PnL on full historical data: ${strategy_total_pnl:.2f}")