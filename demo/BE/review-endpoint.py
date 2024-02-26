from flask import Flask, request, jsonify
from transformers import DistilBertForSequenceClassification, DistilBertConfig, DistilBertTokenizer
import torch
import os
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the Flask app


# Sentiment

# Define paths to model files
sentiment_model_folder_path = './sentiment_model/'
sentiment_config_path = os.path.join(sentiment_model_folder_path, 'config.json')
sentiment_model_path = os.path.join(sentiment_model_folder_path, 'pytorch_model.bin')
sentiment_tokenizer_path =  os.path.join(sentiment_model_folder_path, 'tokenizer.json')

# Load the model configuration
sentiment_config = DistilBertConfig.from_json_file(sentiment_config_path)

# Load the model weights
sentiment_model = DistilBertForSequenceClassification.from_pretrained(sentiment_model_path, config=sentiment_config)

# Load the tokenizer
sentiment_tokenizer = DistilBertTokenizer.from_pretrained(sentiment_tokenizer_path)

# Tokenizer
sentiment_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Define Prediction Function
def sentiment_predict(text):
    inputs = sentiment_tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
    outputs = sentiment_model(**inputs)
    predicted_class = torch.argmax(outputs.logits).item()
    return predicted_class


# Score

# Define paths to model files
regression_model_folder_path = './regression_model/'
regression_config_path = os.path.join(regression_model_folder_path, 'config.json')
regression_model_path = os.path.join(regression_model_folder_path, 'pytorch_model.bin')
regression_tokenizer_path =  os.path.join(regression_model_folder_path, 'tokenizer.json')

# Load the model configuration
regression_config = DistilBertConfig.from_json_file(regression_config_path)

# Check if CUDA is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the regression model
regression_model = DistilBertForSequenceClassification(regression_config)
regression_model.load_state_dict(torch.load(regression_model_path, map_location=device))

# Load the tokenizer
regression_tokenizer = DistilBertTokenizer.from_pretrained(regression_tokenizer_path)

# Tokenizer
regression_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

def regression_predict(text):
    inputs = regression_tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
    outputs = regression_model(**inputs)
    predicted_value = outputs.logits.item()  # Directly use the logits for regression
    return predicted_value



# Top Critic






# Route to handle pre-flight requests
@app.route('/predict-sentiment', methods=['OPTIONS'])
def handle_options():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return ('', 204, headers)

# Actual endpoint to handle POST requests
@app.route('/predict-sentiment', methods=['POST'])
def sentiment_predict_endpoint():
    # Get movie review text from request body
    review_text = request.json.get('review', '')
    
    # Perform sentiment prediction
    sentiment_prediction = sentiment_predict(review_text)
    # Map predicted class to sentiment label
    sentiment_label = "Positive" if sentiment_prediction == 1 else "Medium" if sentiment_prediction == 2 else "Negative" 
    
    # Adjust
    score = regression_predict(review_text)
    
    topCritic = False
    
    # Return sentiment prediction as JSON response
    return jsonify({'sentiment': sentiment_label, 'predictedScore': score, 'topCritic': topCritic})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=8080)
