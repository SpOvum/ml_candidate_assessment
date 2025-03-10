import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import webbrowser

# Load data from the provided CSV file
data = pd.read_csv('C:/Users/mgssr/Desktop/vscode/weight_n2.csv')

# Data cleaning and transformation for the dataset
data['time_stamp'] = pd.to_datetime(data['time_stamp'], format='%Y-%m-%d %H:%M:%S')
numeric_columns = ['n2']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Create directory for saving images
image_dir = 'imagesn2'
os.makedirs(image_dir, exist_ok=True)

# Hourly, weekday, and monthly statistics
hourly_mean = data.groupby(data['time_stamp'].dt.hour)[numeric_columns].mean().rename_axis('hour').reset_index()
hourly_median = data.groupby(data['time_stamp'].dt.hour)[numeric_columns].median().rename_axis('hour').reset_index()
weekday_mean = data.groupby(data['time_stamp'].dt.weekday)[numeric_columns].mean().rename_axis('weekday').reset_index()
weekday_median = data.groupby(data['time_stamp'].dt.weekday)[numeric_columns].median().rename_axis('weekday').reset_index()
monthly_mean = data.groupby(data['time_stamp'].dt.month)[numeric_columns].mean().rename_axis('month').reset_index()
monthly_median = data.groupby(data['time_stamp'].dt.month)[numeric_columns].median().rename_axis('month').reset_index()

# Plot hourly, weekday, and monthly statistics
fig, axs = plt.subplots(4, 2, figsize=(15, 20))

# Hourly plots
axs[0, 0].plot(hourly_mean['hour'], hourly_mean['n2'], label='Mean N2')
axs[0, 0].plot(hourly_median['hour'], hourly_median['n2'], label='Median N2')
axs[0, 0].set_title('N2 Variation by Hour')
axs[0, 0].legend()

# Weekday plots
axs[1, 0].plot(weekday_mean['weekday'], weekday_mean['n2'], label='Mean N2')
axs[1, 0].plot(weekday_median['weekday'], weekday_median['n2'], label='Median N2')
axs[1, 0].set_title('N2 Variation by Weekday')
axs[1, 0].legend()

# Monthly plots
axs[2, 0].plot(monthly_mean['month'], monthly_mean['n2'], label='Mean N2')
axs[2, 0].plot(monthly_median['month'], monthly_median['n2'], label='Median N2')
axs[2, 0].set_title('N2 Variation by Month')
axs[2, 0].legend()

plt.tight_layout()
plt.savefig(f'{image_dir}/variation_plots.png')
plt.close(fig)

# Correlation analysis
correlations = data[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlations, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(f'{image_dir}/correlation_heatmap.png')
plt.close()

# Calendar chart for each year
data['year'] = data['time_stamp'].dt.year
data['month'] = data['time_stamp'].dt.month
data['day'] = data['time_stamp'].dt.day
years = data['year'].unique()

month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

for year in years:
    year_data = data[data['year'] == year]
    daily_data = year_data.groupby(['month', 'day'])['n2'].mean().reset_index()
    pivot_table = daily_data.pivot(index='month', columns='day', values='n2')

    plt.figure(figsize=(15, 8))
    ax = sns.heatmap(pivot_table, cmap='viridis', linewidths=0.5, linecolor='gray', annot=True, fmt=".1f", cbar_kws={'label': 'N2 Value'}, annot_kws={"size": 8})

    ax.set_yticklabels([month_names[m] for m in pivot_table.index], rotation=0)
    plt.title(f'N2 Calendar Chart for {year}')
    plt.xlabel('Day')
    plt.ylabel('Month')
    plt.tight_layout()
    plt.savefig(f'{image_dir}/n2_calendar_chart_{year}.png')
    plt.close()

# Extract date and select relevant variables
data['year'] = data['time_stamp'].dt.year
data['month'] = data['time_stamp'].dt.month
data['day'] = data['time_stamp'].dt.day

# Group by date and count the number of entries
daily_entry_counts = data.groupby(['year', 'month', 'day']).size().reset_index(name='count')

# Convert year, month, and day columns to datetime
daily_entry_counts['date'] = pd.to_datetime(daily_entry_counts[['year', 'month', 'day']])

# Plot the interactive histogram
fig = px.bar(daily_entry_counts, x='date', y='count', labels={'count': 'Number of Entry Points', 'date': 'Date'},
             title='Number of Entry Points Day-wise',
             width=1600, height=800)  # Significantly increased width and height

fig.update_xaxes(type='category')  # Set x-axis type to categorical
fig.write_html(f'{image_dir}/daily_entry_points_histogram.html')

# Define the window sizes for moving averages
window_sizes = {'minute': '1min', 'hour': '1h', 'day': '1d', 'month': 'MS'}

# Separate data for each year
for year in years:
    df_year = data[data['year'] == year]
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
            plt.savefig(f'{image_dir}/moving_avg_plots_{interval}_{year}.png')  # Save all subplots as one figure
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
            <img src="imagesfreezer/variation_plots.png" alt="Variation Plots">
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
            <h2>N2 and {interval.capitalize()} Moving Average - {year}</h2>
            <img src="imagesfreezer/moving_avg_plots_{interval}_{year}.png" alt="N2 and {interval.capitalize()} Moving Average - {year}">
        </div>
        """

for year in years:
    html_content += f"""
        <div class="plot">
            <h2>N2 Calendar Chart for {year}</h2>
            <img src="imagesfreezer/n2_calendar_chart_{year}.png" alt="N2 Calendar Chart for {year}">
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
