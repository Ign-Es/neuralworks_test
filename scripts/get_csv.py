import pandas as pd
from datetime import datetime
import numpy as np


# Specify the path to the CSV file
csv_path = 'data/dataset_SCL.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_path)

# Check for null, NaN, or None values
nan_values = df.isna().sum()
print("\nNaN values:")
print(nan_values)

# Check for duplicate values
duplicate_values = df.duplicated().sum()
print("\nDuplicate values:")
print(duplicate_values)

# Check the position of NaN values
nan_positions = np.where(pd.isnull(df))
print("NaN positions:")
for row, col in zip(nan_positions[0], nan_positions[1]):
    print(f"Row: {row}, Column: {col}")

#Create empty DataFrame to store the new features
synthetic_features = pd.DataFrame()

# Display the head loaded DataFrame
#print(df.head())

# Convert columns to datetime format
df['Fecha-I'] = pd.to_datetime(df['Fecha-I'])
df['Fecha-O'] = pd.to_datetime(df['Fecha-O'])

# Define a function to check if the date is within the given range
def is_within_date_range(dt):
    if dt.month > 12 or (dt.month == 12 and dt.day >= 15):
        return True
    elif dt.month < 3 or (dt.month == 3 and dt.day <= 3):
        return True
    elif (dt.month == 7 and dt.day >= 15 and dt.day <= 31):
        return True
    elif (dt.month == 9 and dt.day >= 11 and dt.day <= 30):
        return True
    else:
        return False

# Create a new column with the result of the function
synthetic_features['Temporada_alta'] = df['Fecha-I'].apply(is_within_date_range)

# Define a function to display the number of repetitions of each unique value in a series
def unique_reps(pd_series):
    value_counts = pd_series.value_counts()
    print("\nRepetitions of Unique Values:")
    for value, count in value_counts.items():
        print(f"{value}: {count}")

# Get the time difference in minutes between the "Fecha-I" and "Fecha-O" columns
synthetic_features['Diferencia_en_minutos'] = (df['Fecha-O'] - df['Fecha-I']).dt.total_seconds() / 60

# Define function to get minor time delays (>15 minutes)
def get_minor_delays(time_dif):
    if time_dif < 15 and time_dif > 0:
        return True
    else:
        return False

# Create a new column with the result of the function
synthetic_features['Atraso_menor'] = synthetic_features['Diferencia_en_minutos'].apply(get_minor_delays)    

# Define time categories
time_categories = {
    'mañana': ((5, 0), (11, 59)),
    'tarde': ((12, 0), (18, 59)),
    'noche': ((19, 0), (4, 59))
}

# Create a function to classify the time
def classify_time(timestamp):
    hour = timestamp.hour
    minute = timestamp.minute

    for category, ((start_hour, start_minute), (end_hour, end_minute)) in time_categories.items():
        if category == 'noche':
            if (hour > start_hour or (hour == start_hour and minute >= start_minute)) or \
                    (hour < end_hour or (hour == end_hour and minute <= end_minute)):
                return category
        else:
            if (hour > start_hour or (hour == start_hour and minute >= start_minute)) and \
                    (hour < end_hour or (hour == end_hour and minute <= end_minute)):
                return category
    return None

# Apply the function to the "Fecha-I" column
synthetic_features['Periodo_dia'] = df['Fecha-I'].apply(classify_time)

# Save synthetic_features DataFrame to a CSV file
synthetic_features.to_csv('results/synthetic_features.csv', index=False)

# Create empty DataFrame to store features that can be useful for model selection
#print(df.columns)
initial_features = df[[ 'Vlo-I', 'Ori-I', 'Des-I', 'Emp-I', 'DIA', 'MES', 'AÑO', 'TIPOVUELO', 'OPERA', 'SIGLAORI', 'SIGLADES']]
initial_features[['Periodo_dia','Temporada_alta']] = synthetic_features[[ 'Periodo_dia','Temporada_alta']] 

# Define function to get which flights are delayed (>0 minutes)
def get_delays(time_dif):
    if time_dif > 0:
        return True
    else:
        return False

# Create a series for target feature    
initial_features['atraso'] = synthetic_features['Diferencia_en_minutos'].apply(get_delays) 

# Get the hour of day of the flight
initial_features['HORA'] = df['Fecha-I'].dt.hour
#print(initial_features.head())

# Save initial_features DataFrame to a CSV file
initial_features.to_csv('data/initial_features.csv', index=False)

