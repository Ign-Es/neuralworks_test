import requests
import json

# Define the API endpoint URL
url = 'http://localhost:5000/predict'

# Define the input data for prediction
data = {
    'Fecha-I': ['2017-01-01 23:30:00'],
    'Vlo-I': ['226'],
    'Ori-I': ['SCEL'],
    'Des-I': ['KMIA'],
    'Emp-I': ['AAL'],
    'DIA': [1],
    'MES': [1],
    'AÑO': [2017],
    'TIPOVUELO': ['I'],
    'OPERA': ['American Airlines'],
    'SIGLAORI': ['Santiago'],
    'SIGLADES': ['Miami']
}

# Send the POST request to the API endpoint
response = requests.post(url, json=data)

try:
    # Try to parse the response as JSON
    predictions = response.json()['predictions']
    print(predictions)
except json.decoder.JSONDecodeError:
    # Print the response content if it's not in valid JSON format
    print(response.content)