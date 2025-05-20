from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

feedback_list = []

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback_text = data.get('feedback')
    rating = data.get('rating')

    blob = TextBlob(feedback_text)
    sentiment = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

    feedback_list.append({
        'feedback': feedback_text,
        'sentiment': sentiment_label,
        'rating': rating
    })

    return jsonify({'message': 'Feedback submitted successfully'}), 200

@app.route('/feedback-summary', methods=['GET'])
def feedback_summary():
    return jsonify(feedback_list), 200

# This part is important for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local, Render sets PORT
    app.run(host='0.0.0.0', port=port)
