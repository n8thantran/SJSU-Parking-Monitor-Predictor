import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the cleaned CSV file
df = pd.read_csv('parkingDataNew.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Function to plot garage fullness for a specific date
def plot_garage_fullness(date_str):
    # Convert input date string to datetime object
    plot_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Filter data for the given date
    day_data = df[df['Date'].dt.date == plot_date.date()]
    
    # Create a new figure
    plt.figure(figsize=(12, 6))
    
    # List of garages and colors
    garages = day_data['Garage'].unique()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    # Plot data for each garage
    for garage, color in zip(garages, colors):
        garage_data = day_data[day_data['Garage'] == garage]
        plt.plot(garage_data['Date'], garage_data['Fullness (%)'], 
                 label=garage, color=color, linewidth=2)
    
    # Customize the plot
    plt.title(f'Garage Fullness on {plot_date.strftime("%Y-%m-%d")}', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Fullness (%)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis to show only time
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    # Set y-axis range from 0 to 100
    plt.ylim(0, 100)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
plot_garage_fullness('2024-09-24')
