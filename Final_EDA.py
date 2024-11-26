# Databricks notebook source
# MAGIC %md
# MAGIC ##Import and Environment Setup

# COMMAND ----------

# MAGIC %pip install ucimlrepo
# MAGIC %pip install 'urllib3<2' 
# MAGIC %pip install 'typing_extensions>=4.5' --upgrade
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import time
import sklearn
import numpy as np
import cloudpickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from ucimlrepo import fetch_ucirepo 
from sklearn.model_selection import train_test_split

# COMMAND ----------

# MAGIC %md
# MAGIC ##Load the Data | Bike Sharing

# COMMAND ----------

# MAGIC %md Feature Descriptions : 
# MAGIC   
# MAGIC 	- instant: record index
# MAGIC 	- dteday : date
# MAGIC 	- season : season (1:springer, 2:summer, 3:fall, 4:winter)
# MAGIC 	- yr : year (0: 2011, 1:2012)
# MAGIC 	- mnth : month ( 1 to 12)
# MAGIC 	- hr : hour (0 to 23)
# MAGIC 	- holiday : weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
# MAGIC 	- weekday : day of the week
# MAGIC 	- workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
# MAGIC 	+ weathersit : 
# MAGIC 		- 1: Clear, Few clouds, Partly cloudy, Partly cloudy
# MAGIC 		- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
# MAGIC 		- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
# MAGIC 		- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
# MAGIC 	- temp : Normalized temperature in Celsius. The values are divided to 41 (max)
# MAGIC 	- atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
# MAGIC 	- hum: Normalized humidity. The values are divided to 100 (max)
# MAGIC 	- windspeed: Normalized wind speed. The values are divided to 67 (max)
# MAGIC 	- casual: count of casual users
# MAGIC 	- registered: count of registered users
# MAGIC 	- cnt: count of total rental bikes including both casual and registered

# COMMAND ----------

# fetch dataset 
bike_sharing = fetch_ucirepo(id=275) 
  
# data (as pandas dataframes) 
X = bike_sharing.data.features 
y = bike_sharing.data.targets 
  
# metadata 
print(bike_sharing.metadata) 
  
# variable information 
print(bike_sharing.variables) 

bike_df = bike_sharing.data.original
bike_df.set_index('dteday', inplace=True)


# COMMAND ----------

# MAGIC %md
# MAGIC ##Preprocessing

# COMMAND ----------

def get_training_data():
  training_data = pd.DataFrame(bike_ref[:'2012-01-01'])
  X = training_data.drop(columns="cnt")
  y = training_data["cnt"]
  return X, y

def get_validation_data():
  validation_data = pd.DataFrame(bike_df['2012-01-01':'2012-06-30'])
  X = validation_data.drop(columns="cnt")
  y = validation_data["cnt"]
  return X, y

def get_weather_and_forecast():
  format_date = lambda pd_date : pd_date.date().strftime("%Y-%m-%d")
  today = pd.Timestamp('dteday').normalize()
  week_ago = today - pd.Timedelta(days=5)
  week_later = today + pd.Timedelta(days=5)

  past_cnt = pd.DataFrame(bike_ref)[format_date(week_ago):format_date(today)]
  weather_and_forecast = pd.DataFrame(bike_ref)[format_date(week_ago):format_date(week_later)]
  if len(weather_and_forecast) < 10:
    past_cnt = pd.DataFrame(bike_ref).iloc[-10:-5]
    weather_and_forecast = pd.DataFrame(bike_ref).iloc[-10:]

  return weather_and_forecast.drop(columns="cnt"), past_power_output["cnt"]

# COMMAND ----------

# MAGIC %md
# MAGIC # EDA

# COMMAND ----------

bike_df.head()

# COMMAND ----------

# Check for missing values
print(bike_df.isnull().sum())

# Display basic statistics
print(bike_df.describe())

pd.set_option('display.max_columns', None)


# COMMAND ----------

# Distribution plot for target variable
plt.figure(figsize=(10, 6))
sns.histplot(bike_df['cnt'], kde=True, bins=30, color = 'purple')
plt.title('Distribution of Bike Rentals')
plt.xlabel('Count')
plt.ylabel('Frequency')
plt.show()


# COMMAND ----------

# Plotting total bike rentals over time
plt.figure(figsize=(14, 8))
bike_df['cnt'].plot(color = 'purple')
plt.title('Bike Rentals Over Time')
plt.xlabel('Date')
plt.ylabel('Count')
plt.grid()
plt.show()


# COMMAND ----------

# Compute correlation matrix
correlation_matrix = bike_df.corr()

# Plotting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='magma', vmin=-1, vmax=1)
plt.title('Feature Correlation Heatmap')
plt.show()


# COMMAND ----------

# Scatterplot for temperature vs. bike rentals
plt.figure(figsize=(8, 5))
sns.scatterplot(x=bike_df['temp'], y=bike_df['cnt'] , color = 'purple')
plt.title('Temperature vs Bike Rentals')
plt.xlabel('Temperature')
plt.ylabel('Bike Rentals')
plt.show()

# Scatterplot for humidity vs. bike rentals
plt.figure(figsize=(8, 5))
sns.scatterplot(x=bike_df['hum'], y=bike_df['cnt'], color = 'lightblue')
plt.title('Humidity vs Bike Rentals')
plt.xlabel('Humidity')
plt.ylabel('Bike Rentals')
plt.show()


# COMMAND ----------

# Rentals by day of the week
plt.figure(figsize=(10, 6))
sns.boxplot(data=bike_df, x='weekday', y='cnt', palette='coolwarm')
plt.title('Bike Rentals by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Count')
plt.show()

# Rentals by season
plt.figure(figsize=(10, 6))
sns.boxplot(data=bike_df, x='season', y='cnt', palette='coolwarm')
plt.title('Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Count')
plt.show()


# COMMAND ----------

# Convert DateTime
#bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
#bike_df.set_index('dteday', inplace=True)
# Ensure the index is in datetime format
bike_df.index = pd.to_datetime(bike_df.index)


# Aggregating bike rentals per month
monthly_rentals = bike_df.resample('M').sum()

plt.figure(figsize=(14, 8))
monthly_rentals['cnt'].plot()
plt.title('Monthly Bike Rentals')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.grid()
plt.show()



# COMMAND ----------

# MAGIC %md
# MAGIC # Feature Engineering

# COMMAND ----------

bike_df.head()


# COMMAND ----------

# Create features for holiday proximity or special events to capture potential rental spikes or drops.
bike_df['day'] = bike_df.index.day
bike_df['week'] = bike_df.index.isocalendar().week
bike_df['quarter'] = bike_df.index.quarter


# COMMAND ----------

# Lag Features: Create lag features for cnt to capture the effect of past rentals on current values.
bike_df['cnt_lag_1'] = bike_df['cnt'].shift(1)
bike_df['cnt_lag_7'] = bike_df['cnt'].shift(7)  # Weekly lag

# COMMAND ----------

# Rolling Statistics: Compute rolling means and standard deviations for cnt or weather features to capture trends.
bike_df['cnt_roll_mean_3'] = bike_df['cnt'].rolling(window=3).mean()
bike_df['cnt_roll_std_3'] = bike_df['cnt'].rolling(window=3).std()

# COMMAND ----------

# Categorical Encoding: Encode season, weekday, mnth, and weathersit using one-hot encoding or ordinal encoding.
bike_df = pd.get_dummies(bike_df, columns=['season', 'weekday', 'mnth', 'weathersit'])

# COMMAND ----------

# Interaction Features: Create interaction terms between temp and humidity for more complex relationships.
bike_df['temp_hum_interaction'] = bike_df['temp'] * bike_df['hum']

# COMMAND ----------

# MAGIC %md
# MAGIC ##
