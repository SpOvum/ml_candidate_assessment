import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import spearmanr, kendalltau, pearsonr
import os
import webbrowser

# Load data
df = pd.read_csv('C:/Users/mgssr/Desktop/vscode/data.csv')
df_room2 = pd.read_csv('C:/Users/mgssr/Desktop/vscode/mane_room_2.csv')
df_room2_2022 = pd.read_csv('C:/Users/mgssr/Desktop/vscode/mane_room_2_2022.csv')
df_room2_2023 = pd.read_csv('C:/Users/mgssr/Desktop/vscode/mane_room_2_2023.csv')
df_room2_2024 = pd.read_csv('C:/Users/mgssr/Desktop/vscode/mane_room_2_2024.csv')

# Drop unnecessary columns
columns_to_drop = ['token', 'uv', 'light', 'weight', 'device_id']

def drop_columns_if_exist(df, columns):
    return df.drop(columns=[col for col in columns if col in df.columns])

df = drop_columns_if_exist(df, columns_to_drop)
df_room2 = drop_columns_if_exist(df_room2, columns_to_drop)
df_room2_2022 = drop_columns_if_exist(df_room2_2022, columns_to_drop)
df_room2_2023 = drop_columns_if_exist(df_room2_2023, columns_to_drop)
df_room2_2024 = drop_columns_if_exist(df_room2_2024, columns_to_drop)

# Data cleaning and transformation for df_room2
df_room2['time_stamp'] = pd.to_datetime(df_room2['time_stamp'], dayfirst=True)
numeric_columns = ['co2', 'humidity', 'temperature', 'voc', 'pressure']

# Check for non-numeric values and remove them
for col in numeric_columns:
    df_room2[col] = pd.to_numeric(df_room2[col], errors='coerce')

# Drop rows with any NaN values in numeric columns
df_room2 = df_room2.dropna(subset=numeric_columns)

# Create directory for saving images
os.makedirs('imagesroom2', exist_ok=True)

# Hourly, weekday, and monthly statistics
hourly_mean = df_room2.groupby(df_room2['time_stamp'].dt.hour).mean().rename_axis('hour').reset_index()
hourly_median = df_room2.groupby(df_room2['time_stamp'].dt.hour).median().rename_axis('hour').reset_index()
weekday_mean = df_room2.groupby(df_room2['time_stamp'].dt.weekday).mean().rename_axis('weekday').reset_index()
weekday_median = df_room2.groupby(df_room2['time_stamp'].dt.weekday).median().rename_axis('weekday').reset_index()
monthly_mean = df_room2.groupby(df_room2['time_stamp'].dt.month).mean().rename_axis('month').reset_index()
monthly_median = df_room2.groupby(df_room2['time_stamp'].dt.month).median().rename_axis('month').reset_index()

# Plot hourly, weekday, and monthly statistics
fig, axs = plt.subplots(8, 2, figsize=(15, 40))

# Hourly plots
axs[0, 0].plot(hourly_mean['hour'], hourly_mean['co2'], label='Mean CO2')
axs[0, 0].plot(hourly_median['hour'], hourly_median['co2'], label='Median CO2')
axs[0, 0].set_title('CO2 Variation by Hour')
axs[0, 0].legend()
axs[0, 1].plot(hourly_mean['hour'], hourly_mean['humidity'], label='Mean Humidity')
axs[0, 1].plot(hourly_median['hour'], hourly_median['humidity'], label='Median Humidity')
axs[0, 1].set_title('Humidity Variation by Hour')
axs[0, 1].legend()

# Weekday plots
axs[1, 0].plot(weekday_mean['weekday'], weekday_mean['co2'], label='Mean CO2')
axs[1, 0].plot(weekday_median['weekday'], weekday_median['co2'], label='Median CO2')
axs[1, 0].set_title('CO2 Variation by Weekday')
axs[1, 0].legend()
axs[1, 1].plot(weekday_mean['weekday'], weekday_mean['humidity'], label='Mean Humidity')
axs[1, 1].plot(weekday_median['weekday'], weekday_median['humidity'], label='Median Humidity')
axs[1, 1].set_title('Humidity Variation by Weekday')
axs[1, 1].legend()

# Monthly plots
axs[2, 0].plot(monthly_mean['month'], monthly_mean['co2'], label='Mean CO2')
axs[2, 0].plot(monthly_median['month'], monthly_median['co2'], label='Median CO2')
axs[2, 0].set_title('CO2 Variation by Month')
axs[2, 0].legend()
axs[2, 1].plot(monthly_mean['month'], monthly_mean['humidity'], label='Mean Humidity')
axs[2, 1].plot(monthly_median['month'], monthly_median['humidity'], label='Median Humidity')
axs[2, 1].set_title('Humidity Variation by Month')
axs[2, 1].legend()

# Additional hourly plots
axs[3, 0].plot(hourly_mean['hour'], hourly_mean['temperature'], label='Mean Temperature')
axs[3, 0].plot(hourly_median['hour'], hourly_median['temperature'], label='Median Temperature')
axs[3, 0].set_title('Temperature Variation by Hour')
axs[3, 0].legend()
axs[4, 0].plot(hourly_mean['hour'], hourly_mean['voc'], label='Mean VOC')
axs[4, 0].plot(hourly_median['hour'], hourly_median['voc'], label='Median VOC')
axs[4, 0].set_title('VOC Variation by Hour')
axs[4, 0].legend()
axs[5, 0].plot(hourly_mean['hour'], hourly_mean['pressure'], label='Mean Pressure')
axs[5, 0].plot(hourly_median['hour'], hourly_median['pressure'], label='Median Pressure')
axs[5, 0].set_title('Pressure Variation by Hour')
axs[5, 0].legend()

# Additional weekday plots
axs[6, 0].plot(weekday_mean['weekday'], weekday_mean['voc'], label='Mean VOC')
axs[6, 0].plot(weekday_median['weekday'], weekday_median['voc'], label='Median VOC')
axs[6, 0].set_title('VOC Variation by Weekday')
axs[6, 0].legend()
axs[7, 0].plot(weekday_mean['weekday'], weekday_mean['pressure'], label='Mean Pressure')
axs[7, 0].plot(weekday_median['weekday'], weekday_median['pressure'], label='Median Pressure')
axs[7, 0].set_title('Pressure Variation by Weekday')
axs[7, 0].legend()

# Additional monthly plots
axs[3, 1].plot(monthly_mean['month'], monthly_mean['temperature'], label='Mean Temperature')
axs[3, 1].plot(monthly_median['month'], monthly_median['temperature'], label='Median Temperature')
axs[3, 1].set_title('Temperature Variation by Month')
axs[3, 1].legend()
axs[4, 1].plot(monthly_mean['month'], monthly_mean['voc'], label='Mean VOC')
axs[4, 1].plot(monthly_median['month'], monthly_median['voc'], label='Median VOC')
axs[4, 1].set_title('VOC Variation by Month')
axs[4, 1].legend()
axs[5, 1].plot(monthly_mean['month'], monthly_mean['pressure'], label='Mean Pressure')
axs[5, 1].plot(monthly_median['month'], monthly_median['pressure'], label='Median Pressure')
axs[5, 1].set_title('Pressure Variation by Month')
axs[5, 1].legend()

plt.tight_layout()
plt.savefig('images/room2_variation_plots.png')
plt.close(fig)

# Correlation analysis
correlations = df_room2[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlations, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig('images/correlation_heatmap.png')
plt.close()

# Calendar chart for each variable and each year
df_room2['year'] = df_room2['time_stamp'].dt.year
df_room2['month'] = df_room2['time_stamp'].dt.month
df_room2['day'] = df_room2['time_stamp'].dt.day
variables = ['co2', 'humidity', 'temperature', 'voc', 'pressure']
years = [2022, 2023, 2024]

month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

for variable in variables:
    for year in years:
        year_data = df_room2[df_room2['year'] == year]
        daily_data = year_data.groupby(['month', 'day'])[variable].mean().reset_index()
        pivot_table = daily_data.pivot(index='month', columns='day', values=variable)

        if not pivot_table.empty:
            plt.figure(figsize=(15, 8))
            ax = sns.heatmap(pivot_table, cmap='viridis', linewidths=0.5, linecolor='gray', annot=True, fmt=".1f", cbar_kws={'label': f'{variable.capitalize()} Value'}, annot_kws={"size": 8})

            ax.set_yticklabels([month_names[m] for m in pivot_table.index], rotation=0)
            plt.title(f'{variable.capitalize()} Calendar Chart for Mane_Room_2 - {year}')
            plt.xlabel('Day')
            plt.ylabel('Month')
            plt.tight_layout()
            plt.savefig(f'images/{variable}_calendar_chart_{year}.png')
            plt.close()

# Extract date and hour
df_room2['date'] = df_room2['time_stamp'].dt.date
df_room2['hour'] = df_room2['time_stamp'].dt.hour

# Group by date and hour and count the number of entries
hourly_entry_counts = df_room2.groupby(['date', 'hour']).size().reset_index(name='count')

# Convert date column to datetime
hourly_entry_counts['date'] = pd.to_datetime(hourly_entry_counts['date'])

# Plot the interactive histogram
fig = px.bar(hourly_entry_counts, x='date', y='count', labels={'count': 'Number of Entry Points', 'date': 'Date'},
             title='Number of Entry Points Hour-wise',
             width=900, height=500)
fig.write_html('images/hourly_entry_counts.html')

# Create HTML file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Room 2 Variation Plots</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 20px auto;
        }
        h1 {
            text-align: center;
            margin: 20px 0;
        }
        .plot {
            margin: 20px 0;
        }
        .plot img {
            width: 100%;
            height: auto;
        }
        .plot iframe {
            width: 100%;
            height: 900px;
            border: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Room 2 Variation Plots</h1>
        <div class="plot">
            <h2>Hourly, Weekday, and Monthly Statistics</h2>
            <img src="images/room2_variation_plots.png" alt="Room 2 Variation Plots">
        </div>
        <div class="plot">
            <h2>Correlation Heatmap</h2>
            <img src="images/correlation_heatmap.png" alt="Correlation Heatmap">
        </div>
        <div class="plot">
            <h2>Number of Entry Points Hour-wise</h2>
            <iframe src="images/hourly_entry_counts.html"></iframe>
        </div>
"""

for variable in variables:
    for year in years:
        html_content += f"""
        <div class="plot">
            <h2>{variable.capitalize()} Calendar Chart for {year}</h2>
            <img src="images/{variable}_calendar_chart_{year}.png" alt="{variable.capitalize()} Calendar Chart for {year}">
        </div>
        """

html_content += """
    </div>
</body>
</html>
"""

with open('room2_variation_plots.html', 'w') as f:
    f.write(html_content)

# Open the HTML file in the default browser
webbrowser.open(f'file://{os.path.realpath("room2_variation_plots.html")}')

