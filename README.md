# Stock Support and Resistance Analysis

`stock_support_resistance_analysis.py` is a Python script that determines the support and resistance levels of a given stock using clustering techniques. The script retrieves stock data from the Alpaca API, calculates peaks and troughs in the stock data, and finds the optimal number of clusters to identify support and resistance levels. Finally, the script plots the stock data with the support and resistance levels indicated.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Technical Description](#technical_description)
4. [Contributing](#contributing)
5. [License](#license)

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

## Technical Description: Part 1 - Data Retrieval and Preprocessing

The script begins by importing the necessary libraries, setting up environment variables for Alpaca API authentication, and initializing the command-line argument parser. The user can specify the stock symbol, number of days to consider, minimum number of clusters, and the clustering method to be used. The script retrieves the stock data using the Alpaca API in the `get_stock_data` function, and calculates the peaks and troughs in the stock data using the `find_peaks_troughs` function, which leverages the `argrelextrema` function from the `scipy` library.

After obtaining the stock data, the code computes the high and low values in the peaks and troughs arrays using the peak_indices and trough_indices arrays. The script then reshapes the peaks and troughs arrays into 2D arrays and calculates the maximum number of clusters for peaks and troughs. With this information, the code can determine the optimal number of clusters for support and resistance levels.

## Technical Description: Part 2 - Clustering and Plotting

The `find_optimal_clusters_silhouette` function calculates the optimal number of clusters based on the silhouette score, a measure of the clustering quality. The function takes the data, minimum number of clusters, maximum number of clusters, and clustering method as arguments. Based on the user's choice, either agglomerative clustering or k-means clustering is used. The script iterates over the range of cluster values and calculates silhouette scores for each number of clusters. The optimal number of clusters corresponds to the highest silhouette score.

Once the optimal number of clusters is determined, the script fits and predicts the clusters using the chosen clustering method (either AgglomerativeClustering or KMeans). It then identifies the cluster the last peak and last trough belong to and computes the maximum high and minimum low of the last peak and trough clusters, respectively, which correspond to the resistance and support levels.

Finally, the script uses Matplotlib to plot the stock data, support and resistance levels, and volume. It displays the stock's high, low, and close prices, along with the support and resistance levels as dashed lines. The peaks and troughs are color-coded based on their cluster group, with markers representing the different clusters. The resulting plot provides a comprehensive view of the stock's historical data, allowing users to visually identify support and resistance levels and inform their trading decisions.
## Technical Description: Part 1 - Data Retrieval and Preprocessing

The script begins by importing the necessary libraries, setting up environment variables for Alpaca API authentication, and initializing the command-line argument parser. The user can specify the stock symbol, number of days to consider, minimum number of clusters, and the clustering method to be used. The script retrieves the stock data using the Alpaca API in the `get_stock_data` function, and calculates the peaks and troughs in the stock data using the `find_peaks_troughs` function, which leverages the `argrelextrema` function from the `scipy` library.

After obtaining the stock data, the code computes the high and low values in the peaks and troughs arrays using the peak_indices and trough_indices arrays. The script then reshapes the peaks and troughs arrays into 2D arrays and calculates the maximum number of clusters for peaks and troughs. With this information, the code can determine the optimal number of clusters for support and resistance levels.

## Technical Description: Part 2 - Clustering and Plotting

The `find_optimal_clusters_silhouette` function calculates the optimal number of clusters based on the silhouette score, a measure of the clustering quality. The function takes the data, minimum number of clusters, maximum number of clusters, and clustering method as arguments. Based on the user's choice, either agglomerative clustering or k-means clustering is used. The script iterates over the range of cluster values and calculates silhouette scores for each number of clusters. The optimal number of clusters corresponds to the highest silhouette score.

Once the optimal number of clusters is determined, the script fits and predicts the clusters using the chosen clustering method (either AgglomerativeClustering or KMeans). It then identifies the cluster the last peak and last trough belong to and computes the maximum high and minimum low of the last peak and trough clusters, respectively, which correspond to the resistance and support levels.

Finally, the script uses Matplotlib to plot the stock data, support and resistance levels, and volume. It displays the stock's high, low, and close prices, along with the support and resistance levels as dashed lines. The peaks and troughs are color-coded based on their cluster group, with markers representing the different clusters. The resulting plot provides a comprehensive view of the stock's historical data, allowing users to visually identify support and resistance levels and inform their trading decisions.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch with your changes
3. Commit your changes to the new branch
4. Create a pull request to merge your changes to the main repository

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

