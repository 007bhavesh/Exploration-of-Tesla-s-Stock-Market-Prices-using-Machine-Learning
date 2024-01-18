# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pandas.plotting import table
import datetime as dt

# Read the CSV file into a Pandas DataFrame
Data = pd.read_csv("/Users/bhaveshtanan/Downloads/TSLA.csv")

# Display the data
Data

# Display data types of each column
Data.dtypes

# Convert the 'Date' column to datetime format
Data['Date'] = pd.to_datetime(Data['Date'])

# Set the display format for float numbers
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Display descriptive statistics of the data
Data.describe(include='all')

# Count the number of missing values in the dataset
Data.isnull().values.sum()

# List of columns for plotting
Column_List= ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Plot stock values over time
Data.plot(x="Date", y=Column_List, subplots=True, layout=(3, 3), figsize=(15, 15),
          sharex=False, title="Stock Value Trend from 2010 - 2020", rot=90)

# Create subplots for distribution plots of each column
fig, ax = plt.subplots(len(Column_List), figsize=(15, 10))
for i, col_list in enumerate(Column_List):
    sns.distplot(Data[col_list], hist=True, ax=ax[i])
    ax[i].set_title("Frequency Distribution of" + " " + col_list, fontsize=10)
    ax[i].set_xlabel(col_list, fontsize=8)
    ax[i].set_ylabel('Distribution Value', fontsize=8)
    fig.tight_layout(pad=1.1)
    ax[i].grid('on')

# Create a heatmap to visualize the correlation matrix
fig, ax = plt.subplots(figsize=(10, 10))
corr_matrix = Data.corr()
sns.heatmap(corr_matrix, xticklabels=corr_matrix.columns.values, yticklabels=corr_matrix.columns.values)

# Display the correlation matrix
corr_matrix

# Create boxplots for outlier detection
fig, ax = plt.subplots(len(Column_List), figsize=(10, 20))
for i, col_list in enumerate(Column_List):
    sns.boxplot(Data[col_list], ax=ax[i], palette="winter", orient="h")
    ax[i].set_title("Whisker Plot for Outlier Detection on" + " " + col_list, fontsize=10)
    ax[i].set_ylabel(col_list, fontsize=8)
    fig.tight_layout(pad=1.1)

# Calculate and display descriptive statistics, and remove outliers using z-score
Descriptive_Statistics = Data.describe()
Descriptive_Statistics = Descriptive_Statistics.T
Descriptive_Statistics['IQR'] = Descriptive_Statistics['75%'] - Descriptive_Statistics['25%']
Data = Data[(np.abs(stats.zscore(Data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']])) < 3).all(axis=1)]
Data = Data.reset_index()

# Display the cleaned data
Data

# Extract year, month, and weekday from the 'Date' column
Data['Year'] = Data['Date'].dt.year
Data['Month'] = Data['Date'].dt.month
Data['WeekDay'] = Data['Date'].dt.weekday

# Create subplots for stock price movement grouped by year
fig, ax = plt.subplots(len(Column_List), figsize=(10, 20))
for i, col_list in enumerate(Column_List):
    Data.groupby('Year')[col_list].plot(ax=ax[i], legend=True)
    ax[i].set_title("Stock Price Movement Grouped By Year on" + " " + col_list, fontsize=10)
    ax[i].set_ylabel(col_list + " " + "Price", fontsize=8)
    fig.tight_layout(pad=1.1)
    ax[i].yaxis.grid(True)

# Plot total volume of stocks traded year-wise
check = Data.groupby('Year')['Volume'].sum()
plt.figure(figsize=(30, 4))
ax1 = plt.subplot(121)
check.plot(y="Volume", legend=False, fontsize=12, sharex=False,
           title="Total Volume of stocks traded Year-wise from 2010-2020", rot=90, color="green")
ax1.ticklabel_format(useOffset=False, style="plain")
ax1.set_ylabel("Total Stock Volumes")
ax1.yaxis.grid(True)

# Plot total volume of stocks traded weekday-wise
check = Data.groupby("WeekDay")['Volume'].sum()
plt.figure(figsize=(30, 4))
ax1 = plt.subplot(121)
check.plot(y="Volume", legend=False, fontsize=12, sharex=False,
           title="Total Volume of Stocks Traded Weekday-wise from 2010 - 2020", rot=90, color="red")
ax1.ticklabel_format(useOffset=False, style="plain")
ax1.set_ylabel("Total Stock Volumes")
ax1.yaxis.grid(True)

# Plot pie charts showing the time series influence on total volume trade
for i, col_list in enumerate(Column_List):
    var = Data.groupby('Year')[col_list].sum()

var = pd.DataFrame(var)

plt.figure(figsize=(16, 7))
ax1 = plt.subplot(121)
var.plot(kind="pie", y="Volume", legend=False, fontsize=12, sharex=False,
         title="Time Series Influence on Total Volume Trade by Year", ax=ax1)

ax2 = plt.subplot(122)
plt.axis('off')
tbl = table(ax2, var, loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
plt.show()

# Repeat the above process for month-wise and weekday-wise total volume trade
for i, col_list in enumerate(Column_List):
    var = Data.groupby('Month')[col_list].sum()

var = pd.DataFrame(var)

plt.figure(figsize=(16, 7))
ax1 = plt.subplot(121)
var.plot(kind="pie", y="Volume", legend=False, fontsize=12, sharex=False,
         title="Time Series Influence on Total Volume Trade by Month", ax=ax1)

ax2 = plt.subplot(122)
plt.axis("off")
tbl = table(ax2, var, loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
plt.show()

for i, col_list in enumerate(Column_List):
    var = Data.groupby('WeekDay')[col_list].sum()

var = pd.DataFrame(var)

plt.figure(figsize=(16, 7))
ax1 = plt.subplot(121)
var.plot(kind="pie", y="Volume", legend=False, fontsize=12, sharex=False,
         title="Time Series Influence on Total Volume Trade by WeekDay", ax=ax1)

ax2 = plt.subplot(122)
plt.axis('off')
tbl = table(ax2, var, loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
plt.show()
