import pandas as pd

def clean_data(file_path):
    # Read the data from the provided file
    df = pd.read_csv(file_path)
    
    # Clean the data
    df['Garage'] = df['Garage'].map({
        'South Garage': 1,
        'West Garage': 2,
        'North Garage': 3,
        'South Campus Garage': 4
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day of the Week'] = df['Date'].dt.dayofweek + 1  # Monday=1, Sunday=7
    df['Seconds Past Midnight'] = df['Date'].dt.hour * 3600 + df['Date'].dt.minute * 60 + df['Date'].dt.second
    
    return df[['Garage', 'Fullness (%)', 'Day of the Week', 'Seconds Past Midnight']]

def save_data(df, output_path):
    df.to_csv(output_path, index=False)

def main():
    input_file = 'data\parkingData.csv'  # Input file path
    output_file = 'data\parkingDataNew.csv'  # Output file path
    
    cleaned_data = clean_data(input_file)
    save_data(cleaned_data, output_file)

if __name__ == '__main__':
    main()
