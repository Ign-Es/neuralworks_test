from flask import Flask, jsonify, request
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, chi2
from custom_functions import is_within_date_range, classify_time


# Load the serialized model
model = joblib.load('models/best_model.pkl')

# Load the preprocessor and feature selector
preprocessor = joblib.load('models/preprocessor.pkl')
feature_selector = joblib.load('models/feature_selector.pkl')

# Create a Flask app
app = Flask(__name__)

# Define an API endpoint for predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the request data
    data = request.json

    # Perform feature encoding and selection on the input data
    X = pd.DataFrame(data)
    X['Fecha-I'] = pd.to_datetime(X['Fecha-I'])
    X['Temporada_alta'] = X['Fecha-I'].apply(is_within_date_range)
    X['Periodo_dia'] = X['Fecha-I'].apply(classify_time)
    X['HORA'] = X['Fecha-I'].dt.hour

    X = X.astype(str)
    X_encoded = preprocessor.transform(X)
    X_selected = feature_selector.transform(X_encoded)

    # Make predictions using the model
    predictions = model.predict_proba(X_selected)

    # Return the predictions as JSON response
    return jsonify({'predictions': predictions.tolist()})

# Run the Flask app
if __name__ == '__main__':
    app.run()