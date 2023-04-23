# Stock Support and Resistance Analysis

`stock_support_resistance_analysis.py` is a Python script that determines the support and resistance levels of a given stock using clustering techniques. The script retrieves stock data from the Alpaca API, calculates peaks and troughs in the stock data, and finds the optimal number of clusters to identify support and resistance levels. Finally, the script plots the stock data with the support and resistance levels indicated.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Summary](#summary)
4. [Contributing](#contributing)
5. [Improvements](#improvements)
6. [Trading](#trading)
7. [License](#license)
7. [Disclaimer](#disclaimer)

## Installation

### Prerequisites

- Python 3.6 or higher
- Alpaca API Key and Secret Key

### Dependencies

The script depends on several Python libraries. You can install them using the following command:

```
pip install numpy pandas matplotlib alpaca-trade-api pandas-market-calendars scipy sklearn
```

### Environment Variables

Set up the following environment variables with your Alpaca API credentials:

```
export APCA_API_KEY_ID=your_alpaca_api_key_id
export APCA_API_SECRET_KEY=your_alpaca_api_secret_key
export APCA_API_BASE_URL=https://paper-api.alpaca.markets # or https://api.alpaca.markets for live trading
```

## Usage

### Command Line Arguments

The script accepts the following command-line arguments:

- `--symbol`: Stock symbol (default: TQQQ)
- `--days_ago`: Number of trading days ago (N). Default is 252 trading days
- `--min_clusters`: Minimum number of clusters (default: 5)
- `--cluster_type`: Clustering method: "agglomerative" or "kmeans" (default: agglomerative)

### Example

```
python stock_support_resistance_analysis.py --symbol TQQQ --days_ago 252 --min_clusters 5 --cluster_type agglomerative
```

This command will fetch stock data for TQQQ for the past 252 trading days and analyze it to determine the support and resistance levels. It will use agglomerative clustering with a minimum of 5 clusters.

## Summary

### Part 1 - Data Retrieval and Preprocessing

The script begins by importing the necessary libraries, setting up environment variables for Alpaca API authentication, and initializing the command-line argument parser. The user can specify the stock symbol, number of days to consider, minimum number of clusters, and the clustering method to be used. The script retrieves the stock data using the Alpaca API in the `get_stock_data` function, and calculates the peaks and troughs in the stock data using the `find_peaks_troughs` function, which leverages the `argrelextrema` function from the `scipy` library.

After obtaining the stock data, the code computes the high and low values in the peaks and troughs arrays using the peak_indices and trough_indices arrays. The script then reshapes the peaks and troughs arrays into 2D arrays and calculates the maximum number of clusters for peaks and troughs. With this information, the code can determine the optimal number of clusters for support and resistance levels.

### Part 2 - Clustering and Plotting

The `find_optimal_clusters_silhouette` function calculates the optimal number of clusters based on the silhouette score, a measure of the clustering quality. The function takes the data, minimum number of clusters, maximum number of clusters, and clustering method as arguments. Based on the user's choice, either agglomerative clustering or k-means clustering is used. The script iterates over the range of cluster values and calculates silhouette scores for each number of clusters. The optimal number of clusters corresponds to the highest silhouette score.

Once the optimal number of clusters is determined, the script fits and predicts the clusters using the chosen clustering method (either AgglomerativeClustering or KMeans). It then identifies the cluster the last peak and last trough belong to and computes the maximum high and minimum low of the last peak and trough clusters, respectively, which correspond to the resistance and support levels.

Finally, the script uses Matplotlib to plot the stock data, support and resistance levels, and volume. It displays the stock's high, low, and close prices, along with the support and resistance levels as dashed lines. The peaks and troughs are color-coded based on their cluster group, with markers representing the different clusters. The resulting plot provides a comprehensive view of the stock's historical data, allowing users to visually identify support and resistance levels and inform their trading decisions.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch with your changes
3. Commit your changes to the new branch
4. Create a pull request to merge your changes to the main repository

## Improvements

### Consider the following suggestions to improve the code for more accurate support and resistance levels.

1. Combine peaks and troughs: Instead of finding support and resistance levels separately for peaks and troughs, you can combine them into one dataset and then cluster. This way, the algorithm will consider both peaks and troughs when finding support and resistance levels, potentially leading to more accurate levels.

2. Use other clustering algorithms: The current code uses Agglomerative Clustering, which is a hierarchical clustering algorithm. You can try other clustering algorithms like DBSCAN or K-Means, which may provide different results, and see which algorithm gives better support and resistance levels for your use case.

3. Consider additional features: You can experiment with adding other technical indicators as features (e.g., RSI, MACD) or consider other market-related information (e.g., trading volume, order book data) when clustering. Make sure to normalize the features to bring them to a similar scale before clustering.

4. Adjust the smoothing parameter: The code currently uses argrelextrema function from scipy.signal to identify peaks and troughs, which uses a comparator function to compare neighboring data points. You can experiment with different comparator functions or adjust the parameters of the current comparator function to find peaks and troughs with varying levels of smoothness.

5. Moving averages: You can use moving averages to smooth out the price data and reduce noise before identifying peaks and troughs. This might help in finding more reliable support and resistance levels.

6. Improve the evaluation metric: Instead of using only the silhouette score, you can try other cluster evaluation metrics like Calinski-Harabasz score or Davies-Bouldin score to determine the optimal number of clusters.

7. Ensemble approach: You can combine the results of different clustering algorithms to create ensemble support and resistance levels. This can potentially lead to more robust and accurate levels.

8. Manual input or domain knowledge: While using an automated approach can be beneficial, incorporating human expertise or manual input based on domain knowledge can help refine the support and resistance levels identified by the algorithm.

## Trading

Support and resistance levels are significant price levels at which a stock tends to reverse its direction or experience increased buying and selling pressure. These levels can be used to make informed trading decisions by identifying potential entry and exit points.

### Here's a general outline on how to use support and resistance levels in stock trading:

1. Identify support and resistance levels: Analyze historical price data and chart patterns to identify key support and resistance levels. You can use tools like horizontal trendlines, moving averages, or Fibonacci retracements to help spot these levels.

2. Entry points:

- When a stock approaches a support level and shows signs of bouncing off that level (e.g., the formation of a bullish candlestick pattern or increased buying volume), it could be a potential buying opportunity. The idea is that the support level will hold, and the price will rebound upwards.
- Conversely, when a stock approaches a resistance level and shows signs of reversing (e.g., bearish candlestick pattern or increased selling volume), it could signal a potential short-selling opportunity. The expectation is that the resistance level will hold, and the price will drop.

3. Exit points:

- If you're in a long position, consider taking profits or tightening your stop-loss order when the price approaches a significant resistance level. There's a higher probability of the stock reversing or consolidating at these levels.
- If you're in a short position, consider covering your short or tightening your stop-loss order when the price approaches a support level, as the stock may reverse or consolidate at these points.

4. Stop-loss orders: Place stop-loss orders below support levels (for long positions) or above resistance levels (for short positions) to protect against unexpected price movements. If the stock breaches the support or resistance level, it may signal a change in market sentiment or a continuation of the trend, which could result in further price movement against your position.

5. Confirmations: Use additional technical indicators and chart patterns to confirm the strength of support and resistance levels. For example, indicators like the Relative Strength Index (RSI), Stochastic Oscillator, or Moving Average Convergence Divergence (MACD) can help confirm trend reversals and momentum shifts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Disclaimer

### Legal Disclaimer

This script is for educational purposes only and is not intended to be used as financial or investment advice. Use this tool at your own risk. The author is not responsible for any financial losses or damages incurred as a result of using this tool. Always consult a financial professional before making any investment decisions.

