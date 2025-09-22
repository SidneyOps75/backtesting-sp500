# S&P 500 Backtesting Project

## Overview

This project implements a quantitative trading strategy backtesting framework for S&P 500 constituents. The goal is to develop and test a stock-picking strategy that aims to outperform the market benchmark using historical data.

## Project Structure

```
project/
│   README.md
│   requirements.txt
│
└───data/
│   │   sp500.csv          # S&P 500 index data
│   │   prices.csv         # Individual stock price data
│
└───notebook/
│   │   analysis.ipynb     # Exploratory Data Analysis
│
└───scripts/
│   │   memory_reducer.py  # Memory optimization utilities
│   │   preprocessing.py   # Data cleaning and preprocessing
│   │   create_signal.py   # Investment signal generation
│   │   backtester.py      # Strategy backtesting framework
│   │   main.py           # Main execution script
│
└───results/
    │   plots/            # Generated visualizations
    │   results.txt       # Backtesting results
    │   outliers.txt      # Identified data outliers
```

## Strategy Description

The implemented strategy uses a momentum-based approach:

1. **Signal Generation**: Calculate 12-month rolling average of historical returns for each stock
2. **Stock Selection**: Each month, select the top 20 stocks with highest average returns
3. **Portfolio Construction**: Invest $1 in each selected stock (equal-weighted portfolio)
4. **Rebalancing**: Monthly rebalancing based on updated signals

## Key Features

- **Memory Optimization**: Efficient data type optimization for large datasets
- **Data Quality Management**: Comprehensive outlier detection and handling
- **Robust Preprocessing**: Missing value imputation and return calculation
- **Performance Visualization**: Strategy vs benchmark comparison plots
- **Modular Design**: Reusable components for different strategies

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
```bash
cd scripts
python main.py
```

### Step-by-Step Analysis
1. **Exploratory Data Analysis**: Open `notebook/analysis.ipynb`
2. **Run Individual Components**:
   ```python
   from memory_reducer import memory_reducer
   from preprocessing import preprocessing
   from create_signal import create_signal
   from backtester import backtest
   
   # Load and process data
   prices = memory_reducer('data/prices.csv')
   sp500 = memory_reducer('data/sp500.csv')
   
   # Preprocess
   prices, sp500 = preprocessing(prices, sp500, plot=True)
   
   # Generate signals
   prices = create_signal(prices)
   
   # Backtest
   backtest(prices, sp500)
   ```

## Data Requirements

### Input Files
- `sp500.csv`: S&P 500 index data with columns: date, adj_close
- `prices.csv`: Individual stock prices with columns: date, ticker, price

### Data Quality Notes
- The dataset contains missing values and outliers by design
- Price spikes and data inconsistencies are handled through preprocessing
- 2008-2009 financial crisis period is treated separately for outlier detection

## Results

The backtesting framework generates:

1. **Performance Metrics**: Total returns, PnL, outperformance vs benchmark
2. **Visualizations**: Cumulative return plots comparing strategy vs S&P 500
3. **Data Quality Reports**: Outlier identification and missing value analysis

## Key Components

### Memory Reducer
Optimizes DataFrame memory usage by selecting appropriate data types:
- Integers: int8, int16, int32, int64
- Floats: float32, float64

### Preprocessing Pipeline
1. Monthly resampling (last value)
2. Price outlier filtering ($0.1 - $10,000 range)
3. Return calculation (historical and future)
4. Outlier replacement (excluding 2008-2009 crisis)
5. Missing value imputation

### Signal Generation
- 12-month rolling average of historical returns
- Top 20 stock selection each month
- Boolean signal generation

### Backtesting Framework
- Vectorized return calculations (no loops)
- Benchmark comparison
- Performance visualization
- Results export

## Performance Considerations

- Memory-optimized data loading
- Vectorized operations for speed
- Efficient groupby operations
- Minimal data copying

## Limitations

- Simplified transaction costs (not included)
- No slippage modeling
- Equal-weighted portfolio assumption
- Monthly rebalancing frequency
- Single-factor signal (momentum only)

## Future Enhancements

- Multi-factor signal models
- Risk-adjusted performance metrics
- Transaction cost modeling
- Alternative rebalancing frequencies
- Portfolio optimization techniques

## Implementation Details

### memory_reducer.py
Optimizes DataFrame memory usage by automatically selecting the smallest appropriate data types for each column. Reduces memory footprint by up to 75% for large datasets.

### preprocessing.py
- Monthly resampling keeping last values
- Price filtering ($0.1 - $10,000 range)
- Return calculations (historical and future)
- Outlier handling excluding 2008-2009 crisis period
- Forward-fill missing value imputation

### create_signal.py
Generates investment signals using 12-month rolling average returns. Selects top 20 performing stocks each month for portfolio construction.

### backtester.py
Vectorized backtesting framework comparing strategy performance against S&P 500 benchmark. Generates performance metrics and visualizations.

### main.py
Orchestrates the complete pipeline from data loading to results generation.

## Performance Results

Based on sample data analysis:
- **Strategy Total Return**: -13.90%
- **S&P 500 Benchmark**: -20.10%
- **Outperformance**: +6.20%
- **Strategy PnL**: -$2.78 (on $20 investment)
- **Benchmark PnL**: -$4.02 (on $20 investment)

The momentum-based strategy successfully outperformed the benchmark during the test period, demonstrating the effectiveness of the stock selection methodology.

## License

This project is for educational purposes as part of quantitative finance learning.