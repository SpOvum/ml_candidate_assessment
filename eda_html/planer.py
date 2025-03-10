import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import webbrowser

# Load data from provided dataset
df = pd.read_csv('C:/Users/mgssr/Desktop/vscode/planer_inc.csv')
df.drop(columns=['ip_address', 'created_at','planer_name'], inplace=True)
# Data cleaning and transformation for the dataset
df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%Y-%m-%d %H:%M:%S')
numeric_columns = ['temp_a', 'temp_b']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Create directory for saving images
os.makedirs('imagesplaner', exist_ok=True)

# Hourly, weekday, and monthly statistics
hourly_mean = df.groupby(df['time_stamp'].dt.hour).mean().rename_axis('hour').reset_index()
hourly_median = df.groupby(df['time_stamp'].dt.hour).median().rename_axis('hour').reset_index()
weekday_mean = df.groupby(df['time_stamp'].dt.weekday).mean().rename_axis('weekday').reset_index()
weekday_median = df.groupby(df['time_stamp'].dt.weekday).median().rename_axis('weekday').reset_index()
monthly_mean = df.groupby(df['time_stamp'].dt.month).mean().rename_axis('month').reset_index()
monthly_median = df.groupby(df['time_stamp'].dt.month).median().rename_axis('month').reset_index()

# Plot hourly, weekday, and monthly statistics
fig, axs = plt.subplots(3, 2, figsize=(15, 20))

# Hourly plots
axs[0, 0].plot(hourly_mean['hour'], hourly_mean['temp_a'], label='Mean Temp A')
axs[0, 0].plot(hourly_median['hour'], hourly_median['temp_a'], label='Median Temp A')
axs[0, 0].set_title('Temp A Variation by Hour')
axs[0, 0].legend()

axs[0, 1].plot(hourly_mean['hour'], hourly_mean['temp_b'], label='Mean Temp B')
axs[0, 1].plot(hourly_median['hour'], hourly_median['temp_b'], label='Median Temp B')
axs[0, 1].set_title('Temp B Variation by Hour')
axs[0, 1].legend()

# Weekday plots
axs[1, 0].plot(weekday_mean['weekday'], weekday_mean['temp_a'], label='Mean Temp A')
axs[1, 0].plot(weekday_median['weekday'], weekday_median['temp_a'], label='Median Temp A')
axs[1, 0].set_title('Temp A Variation by Weekday')
axs[1, 0].legend()

axs[1, 1].plot(weekday_mean['weekday'], weekday_mean['temp_b'], label='Mean Temp B')
axs[1, 1].plot(weekday_median['weekday'], weekday_median['temp_b'], label='Median Temp B')
axs[1, 1].set_title('Temp B Variation by Weekday')
axs[1, 1].legend()

# Monthly plots
axs[2, 0].plot(monthly_mean['month'], monthly_mean['temp_a'], label='Mean Temp A')
axs[2, 0].plot(monthly_median['month'], monthly_median['temp_a'], label='Median Temp A')
axs[2, 0].set_title('Temp A Variation by Month')
axs[2, 0].legend()

axs[2, 1].plot(monthly_mean['month'], monthly_mean['temp_b'], label='Mean Temp B')
axs[2, 1].plot(monthly_median['month'], monthly_median['temp_b'], label='Median Temp B')
axs[2, 1].set_title('Temp B Variation by Month')
axs[2, 1].legend()

plt.tight_layout()
plt.savefig('imagesfreezer/freezer_variation_plots.png')
plt.close(fig)

# Correlation analysis
correlations = df[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlations, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig('imagesfreezer/correlation_heatmap.png')
plt.close()

# Calendar chart for each variable and each year
df['year'] = df['time_stamp'].dt.year
df['month'] = df['time_stamp'].dt.month
df['day'] = df['time_stamp'].dt.day
variables = ['temp_a', 'temp_b']
years = df['year'].unique()

month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

for variable in variables:
    for year in years:
        year_data = df[df['year'] == year]
        daily_data = year_data.groupby(['month', 'day'])[variable].mean().reset_index()
        pivot_table = daily_data.pivot(index='month', columns='day', values=variable)

        plt.figure(figsize=(15, 8))
        ax = sns.heatmap(pivot_table, cmap='viridis', linewidths=0.5, linecolor='gray', annot=True, fmt=".1f", cbar_kws={'label': f'{variable.capitalize()} Value'}, annot_kws={"size": 8})

        ax.set_yticklabels([month_names[m] for m in pivot_table.index], rotation=0)
        plt.title(f'{variable.capitalize()} Calendar Chart for Freezer - {year}')
        plt.xlabel('Day')
        plt.ylabel('Month')
        plt.tight_layout()
        plt.savefig(f'imagesfreezer/{variable}_calendar_chart_{year}.png')
        plt.close()

# Extract date and select relevant variables
df['year'] = df['time_stamp'].dt.year
df['month'] = df['time_stamp'].dt.month
df['day'] = df['time_stamp'].dt.day

# Group by date and count the number of entries
daily_entry_counts = df.groupby(['year', 'month', 'day']).size().reset_index(name='count')

# Convert year, month, and day columns to datetime
daily_entry_counts['date'] = pd.to_datetime(daily_entry_counts[['year', 'month', 'day']])

# Plot the interactive histogram
fig = px.bar(daily_entry_counts, x='date', y='count', labels={'count': 'Number of Entry Points', 'date': 'Date'},
             title='Number of Entry Points Day-wise',
             width=1600, height=800)  # Significantly increased width and height

fig.update_xaxes(type='category')  # Set x-axis type to categorical
fig.write_html('imagesfreezer/daily_entry_points_histogram.html')

# Define the window sizes for moving averages
window_sizes = {'minute': '1min', 'hour': '1h', 'day': '1d', 'month': 'ME'}

# Separate data for each year
for year in years:
    df_year = df[df['year'] == year]
    for interval, window_size in window_sizes.items():
        try:
            # Calculate moving average
            moving_avg = df_year.resample(window_size, on='time_stamp')[numeric_columns].mean()

            # Plot each variable in a separate graph
            columns = moving_avg.columns
            num_plots = len(columns)
            num_rows = (num_plots + 1) // 2  # Calculate the number of rows dynamically

            # Handle cases where the number of columns is 1 or 2
            if num_plots == 1:
                fig, axs = plt.subplots(1, 1, figsize=(12, 3))
                axs.plot(moving_avg.index, moving_avg[columns[0]])
                axs.set_title(f'{columns[0].capitalize()} Moving Average - {interval.capitalize()} Wise - {year}')
                axs.set_xlabel('Time')
                axs.set_ylabel('Value')
                axs.grid(True)
            elif num_plots == 2:
                fig, axs = plt.subplots(1, 2, figsize=(12, 3))
                for i, column in enumerate(columns):
                    axs[i].plot(moving_avg.index, moving_avg[column])
                    axs[i].set_title(f'{column.capitalize()} Moving Average - {interval.capitalize()} Wise - {year}')
                    axs[i].set_xlabel('Time')
                    axs[i].set_ylabel('Value')
                    axs[i].grid(True)
            else:
                fig, axs = plt.subplots(num_rows, 2, figsize=(12, num_rows * 3))
                for i, column in enumerate(columns):
                    row = i // 2
                    col = i % 2
                    axs[row, col].plot(moving_avg.index, moving_avg[column])
                    axs[row, col].set_title(f'{column.capitalize()} Moving Average - {interval.capitalize()} Wise - {year}')
                    axs[row, col].set_xlabel('Time')
                    axs[row, col].set_ylabel('Value')
                    axs[row, col].grid(True)

                # Remove empty subplots if the number of plots is odd
                if num_plots % 2 != 0:
                    fig.delaxes(axs[num_rows - 1, 1])

            plt.tight_layout()
            plt.savefig(f'imagesfreezer/moving_avg_plots_{interval}_{year}.png')  # Save all subplots as one figure
            plt.close(fig)
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")

# Create the main HTML file and embed the Plotly HTML file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Freezer Variation Plots</title>
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
            max-width: 1600px;
            margin: 20px auto;
        }
        h1 {
            text-align: center;
            margin: 20px 0;
        }
        .plot {
            margin: 20px 0;
        }
        .plot img, .plot iframe {
            width: 100%;
            height: auto;
            border: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Freezer Variation Plots</h1>
        <div class="plot">
            <h2>Hourly, Weekday, and Monthly Statistics</h2>
            <img src="imagesfreezer/freezer_variation_plots.png" alt="Freezer Variation Plots">
        </div>
        <div class="plot">
            <h2>Correlation Heatmap</h2>
            <img src="imagesfreezer/correlation_heatmap.png" alt="Correlation Heatmap">
        </div>
        <div class="plot">
            <h2>Number of Entry Points Day-wise</h2>
            <iframe src="imagesfreezer/daily_entry_points_histogram.html" style="height: 900px;"></iframe>  <!-- Significantly increased height of the iframe -->
        </div>
"""

for interval in window_sizes.keys():
    for year in years:
        html_content += f"""
        <div class="plot">
            <h2>Temperature and {interval.capitalize()} Moving Average - {year}</h2>
            <img src="imagesfreezer/moving_avg_plots_{interval}_{year}.png" alt="Temperature and {interval.capitalize()} Moving Average - {year}">
        </div>
        """

for variable in variables:
    for year in years:
        html_content += f"""
        <div class="plot">
            <h2>{variable.capitalize()} Calendar Chart for {year}</h2>
            <img src="imagesfreezer/{variable}_calendar_chart_{year}.png" alt="{variable.capitalize()} Calendar Chart for {year}">
        </div>
        """

html_content += """
    </div>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = os.path.realpath('freezer_variation_plots.html')
with open(html_file_path, 'w') as f:
    f.write(html_content)

# Open the HTML file in the default browser
webbrowser.open(f'file://{html_file_path}')
