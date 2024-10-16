import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

# Load the dataset
# Assuming the dataset is downloaded from Kaggle and saved as 'suicide_watch.csv'
data = pd.read_csv('datasets/Suicide_Detection.csv')

# Preprocessing: Fill missing values and rename columns if necessary
data = data.dropna(subset=['text'])  # Drop rows with missing text

# Features and labels
X = data['text']
# Create labels: Assuming binary classification (1 for high risk, 0 for low risk)
y = data['class']  # Replace 'label' with the actual column name in the dataset if different

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF Vectorizer and Naive Bayes classifier
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
    ('nb', MultinomialNB()),
])

# Train the model
model_pipeline.fit(X_train, y_train)

# Evaluate the model (optional)
accuracy = model_pipeline.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model to a file
model_path = os.path.join(os.path.dirname(__file__), 'models/suicide_model.pkl')
with open(model_path, 'wb') as model_file:
    pickle.dump(model_pipeline, model_file)

print(f"Model training complete and saved as '{model_path}'")
