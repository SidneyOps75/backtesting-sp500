#!/usr/bin/env python3
"""
S&P 500 Backtesting Project
Main execution script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_reducer import memory_reducer
from preprocessing import preprocessing
from create_signal import create_signal
from backtester import backtest

def main():
    """Main execution function."""
    print("Starting S&P 500 Backtesting Analysis...")
    
    # Data file paths
    prices_path = '../data/prices.csv'
    sp500_path = '../data/sp500.csv'
    
    # Check if data files exist
    if not os.path.exists(prices_path):
        print(f"Error: {prices_path} not found. Please add the data files to the data/ directory.")
        return
    
    if not os.path.exists(sp500_path):
        print(f"Error: {sp500_path} not found. Please add the data files to the data/ directory.")
        return
    
    # Import and optimize data
    print("Loading and optimizing data...")
    prices = memory_reducer(prices_path)
    sp500 = memory_reducer(sp500_path)
    
    print(f"Prices data shape: {prices.shape}")
    print(f"S&P 500 data shape: {sp500.shape}")
    
    # Preprocessing
    print("Preprocessing data...")
    prices, sp500 = preprocessing(prices, sp500, plot=True)
    
    print(f"Processed prices shape: {prices.shape}")
    print(f"Processed S&P 500 shape: {sp500.shape}")
    
    # Create signal
    print("Creating investment signal...")
    prices = create_signal(prices)
    
    # Backtest
    print("Running backtest...")
    backtest(prices, sp500)
    
    print("Analysis complete! Check the results/ directory for outputs.")

if __name__ == "__main__":
    main()