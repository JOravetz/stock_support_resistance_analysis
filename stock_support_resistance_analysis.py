#! /usr/bin/env python3

import os
import sys
import datetime
import argparse
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
import pandas_market_calendars as mcal

from scipy.signal import argrelextrema
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering

warnings.filterwarnings("ignore")

# Get stock data from Alpaca API
def get_stock_data(ticker, start_date, end_date):
    api_key = os.getenv("APCA_API_KEY_ID")
    api_secret = os.getenv("APCA_API_SECRET_KEY")
    base_url = os.getenv("APCA_API_BASE_URL")

    api = tradeapi.REST(api_key, api_secret, base_url, api_version="v2")
    stock_data = api.get_bars(
        ticker, TimeFrame.Day, start=start_date, end=end_date
    ).df

    return stock_data


# Determine the optimal number of clusters for support and resistance levels
def find_optimal_clusters_silhouette(
    data, min_clusters, max_clusters, method="agglomerative"
):
    cluster_range = range(min_clusters, max_clusters + 1)

    if method == "agglomerative":
        clustering_function = AgglomerativeClustering
    elif method == "kmeans":
        clustering_function = KMeans
    else:
        raise ValueError(
            "Invalid clustering method. Choose either 'agglomerative' or 'kmeans'."
        )

    silhouette_scores = [
        silhouette_score(
            data, clustering_function(n_clusters=i).fit(data).labels_
        )
        for i in cluster_range
    ]

    optimal_clusters = cluster_range[np.argmax(silhouette_scores)]
    return optimal_clusters


# Find peaks and troughs in the stock data
def find_peaks_troughs(stock_data):
    highs = stock_data["high"].values
    lows = stock_data["low"].values

    peak_indices = argrelextrema(highs, np.greater)
    trough_indices = argrelextrema(lows, np.less)

    peaks = highs[peak_indices]
    troughs = lows[trough_indices]

    return peaks, troughs, peak_indices, trough_indices


# Initialize and parse command line arguments
parser = argparse.ArgumentParser(
    description="Determine the optimal number of clusters for stock support and resistance levels."
)
parser.add_argument(
    "--symbol", type=str, default="TQQQ", help="Stock symbol (default: TQQQ)."
)
parser.add_argument(
    "--days_ago",
    type=int,
    default=252,
    help="Number of trading days ago (N). Default is 252 trading days.",
)
parser.add_argument(
    "--min_clusters",
    type=int,
    default=5,
    help="Minimum number of clusters (default: 5).",
)
parser.add_argument(
    "--cluster_type",
    type=str,
    default="agglomerative",
    help='Clustering method: "agglomerative" or "kmeans" (default: agglomerative).',
)
args = parser.parse_args()

ticker = args.symbol.upper()

clustering_method = args.cluster_type.lower()
if clustering_method not in ["agglomerative", "kmeans"]:
    raise ValueError(
        "Invalid clustering method. Choose either 'agglomerative' or 'kmeans'."
    )

if clustering_method == "kmeans":
    from sklearn.cluster import KMeans

# Get the NYSE calendar and trading schedule
nyse = mcal.get_calendar("NYSE")
schedule = nyse.schedule(
    start_date=datetime.now() - timedelta(days=365), end_date=datetime.now()
)

if len(schedule) == 0:
    schedule = nyse.schedule(
        start_date=datetime.now() - timedelta(days=365 * 2),
        end_date=datetime.now() - timedelta(days=365),
    )

end_date = schedule.index[-1].date()
start_date = end_date - timedelta(days=args.days_ago)

print(
    f"The trading date {args.days_ago} days ago from {end_date} is: {start_date}"
)

# Retrieve stock data and calculate peaks and troughs
stock_data = get_stock_data(ticker, start_date, end_date)
peaks, troughs, peak_indices, trough_indices = find_peaks_troughs(stock_data)

peaks, troughs = np.reshape(peaks, (-1, 1)), np.reshape(troughs, (-1, 1))

min_clusters = args.min_clusters
max_clusters_peaks = len(peaks) - 1
max_clusters_troughs = len(troughs) - 1

# Find the optimal number of clusters for peaks and troughs
optimal_clusters_peaks = find_optimal_clusters_silhouette(
    peaks, min_clusters, max_clusters_peaks, method=clustering_method
)
optimal_clusters_troughs = find_optimal_clusters_silhouette(
    troughs, min_clusters, max_clusters_troughs, method=clustering_method
)

print(f"Optimal number of clusters for peaks: {optimal_clusters_peaks}")
print(f"Optimal number of clusters for troughs: {optimal_clusters_troughs}")

if clustering_method == "agglomerative":
    ac_peaks = AgglomerativeClustering(n_clusters=optimal_clusters_peaks)
    ac_troughs = AgglomerativeClustering(n_clusters=optimal_clusters_troughs)
elif clustering_method == "kmeans":
    ac_peaks = KMeans(n_clusters=optimal_clusters_peaks)
    ac_troughs = KMeans(n_clusters=optimal_clusters_troughs)
else:
    raise ValueError(
        "Invalid clustering method. Choose either 'agglomerative' or 'kmeans'."
    )

peak_labels = ac_peaks.fit_predict(peaks)
trough_labels = ac_troughs.fit_predict(troughs)

# Determine which cluster the last peak belongs to
last_peak = peaks[-1]
peak_cluster_label = peak_labels[-1]

# Find the max high of the last peak cluster group
max_high_peak_cluster = np.max(peaks[peak_labels == peak_cluster_label])

# Determine which cluster the last trough belongs to
last_trough = troughs[-1]
trough_cluster_label = trough_labels[-1]

# Find the min low of the last trough cluster group
min_low_trough_cluster = np.min(
    troughs[trough_labels == trough_cluster_label]
)

# Print the results
print(f"Last peak belongs to Peak Cluster {peak_cluster_label+1}")
print(f"Max high of the last peak cluster group: {max_high_peak_cluster:.2f}")
print(f"Last trough belongs to Trough Cluster {trough_cluster_label+1}")
print(
    f"Min low of the last trough cluster group: {min_low_trough_cluster:.2f}"
)

# Plot the stock data with support and resistance levels
fig, (ax1, ax2) = plt.subplots(
    nrows=2, ncols=1, figsize=(14, 12), gridspec_kw={"height_ratios": [3, 1]}
)

# Plot the price data with support and resistance levels
ax1.plot(stock_data.index, stock_data["high"], label="High")
ax1.plot(stock_data.index, stock_data["low"], label="Low")
ax1.plot(stock_data.index, stock_data["close"], label="Close")
# ax1.plot(stock_data.index, stock_data['vwap'], label='VWAP', linestyle='-', linewidth=2, color='purple')

# Color code the peak and trough points by cluster group
colors_peaks = np.asarray(plt.get_cmap("tab10").colors)[peak_labels % 10]
ax1.scatter(
    stock_data.index[peak_indices[0]], peaks, color=colors_peaks, marker="^"
)

colors_troughs = np.asarray(plt.get_cmap("tab10").colors)[trough_labels % 10]
ax1.scatter(
    stock_data.index[trough_indices[0]],
    troughs,
    color=colors_troughs,
    marker="v",
)

# Plot the support and resistance levels
ax1.hlines(
    min_low_trough_cluster,
    stock_data.index.min(),
    stock_data.index.max(),
    colors="green",
    linestyles="dashed",
    label="Support",
)
ax1.hlines(
    max_high_peak_cluster,
    stock_data.index.min(),
    stock_data.index.max(),
    colors="red",
    linestyles="dashed",
    label="Resistance",
)

# Add text for support and resistance levels
gap_multiplier = 0.020  # Adjust this value to control the gap size
price_range = stock_data["high"].max() - stock_data["low"].min()

ax1.text(
    stock_data.index[0],
    min_low_trough_cluster - (1.5 * gap_multiplier) * price_range,
    f"Support: {min_low_trough_cluster:.3f}",
    color="green",
    fontsize=10,
)
ax1.text(
    stock_data.index[0],
    max_high_peak_cluster + (0.5 * gap_multiplier) * price_range,
    f"Resistance: {max_high_peak_cluster:.3f}",
    color="red",
    fontsize=10,
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Price")
ax1.set_title(
    f'{ticker} Stock Price with Support and Resistance Levels - Close Price: {stock_data["close"][-1]:.3f}'
)
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)

# Plot the volume data
volume = stock_data["volume"]
volume_norm = volume / volume.max()
ax2.vlines(stock_data.index, 0, volume_norm, color="black", alpha=0.5)
ax2.fill_between(stock_data.index, volume_norm, 0, color="black", alpha=0.5)
ax2.set_ylim([0, 1])
ax2.set_xlabel("Date")
ax2.set_ylabel("Volume")
ax2.grid(True, linestyle="--", alpha=0.5)

plt.subplots_adjust(hspace=0.25)
plt.tight_layout()
plt.show()
