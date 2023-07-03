import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, chi2
import joblib

# Step 1: Load the data from the CSV file
data = pd.read_csv('data/initial_features.csv')
# Step 2: Perform feature encoding and selection
X = data.drop('atraso', axis=1)
y = data['atraso']

# Convert all features to strings
X = X.astype(str)

# Categorical feature encoding
categorical_features = ['Vlo-I', 'Ori-I', 'Des-I', 'Emp-I', 'TIPOVUELO', 'OPERA', 'SIGLAORI', 'SIGLADES', 'Periodo_dia', 'Temporada_alta']

preprocessor = ColumnTransformer([
    ('encoder', OneHotEncoder(), categorical_features)
])

X_encoded = preprocessor.fit_transform(X)

# Feature selection using chi-square test for categorical features
feature_selector = SelectKBest(chi2, k='all')
X_selected = feature_selector.fit_transform(X_encoded, y)

# Get selected feature names
selected_feature_names = []
for selected, feature_name in zip(feature_selector.get_support(), preprocessor.get_feature_names_out()):
    if selected:
        selected_feature_names.append(feature_name)

print("Selected Features:", selected_feature_names)

# Step 3: Train and evaluate the models
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Define models with default hyperparameters
models = [
    ('Logistic Regression', LogisticRegression()),
    ('Random Forest', RandomForestClassifier()),
    ('Gradient Boosting', GradientBoostingClassifier())
]

best_model = None
best_score = 0.0

# Train and evaluate models, and select the best-performing model based on the chosen metric
for model_name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)

    print("Model:", model_name)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 score:", f1)
    print("ROC AUC score:", roc_auc)
    print()
    
    # Check if this model outperforms the current best model
    if accuracy > best_score:
        best_model = model
        best_score = accuracy

print("Best Model:", best_model)
print("Best Accuracy:", best_score)

# Serialize the best model
joblib.dump(best_model, 'models/best_model.pkl')

# Serialize the preprocessor
joblib.dump(preprocessor, 'models/preprocessor.pkl')

# Serialize the feature selector
joblib.dump(feature_selector, 'models/feature_selector.pkl')