# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from news_summarizer import fetch_article, summarize_text

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable cross-orig


# in requests to allow your frontend to communicate with the backend

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.json

    # Get number of sentences for the summary
    num_sentences = int(data.get('sentences', 5))

    # Determine if we're processing a URL or direct text
    if 'url' in data and data['url']:
        # Summarize from URL
        print(f"Fetching article from URL: {data['url']}")
        article_text = fetch_article(data['url'])
    elif 'text' in data and data['text']:
        # Summarize from text
        print("Processing provided text")
        article_text = data['text']
    else:
        return jsonify({'error': 'No URL or text provided'}), 400

    if not article_text:
        return jsonify({'error': 'Failed to obtain article text'}), 400

    # Generate summary
    print(f"Generating summary with {num_sentences} sentences...")
    summary = summarize_text(article_text, num_sentences)

    # Count words for the metadata
    word_count = len(summary.split())

    return jsonify({
        'summary': summary,
        'sentences': num_sentences,
        'words': word_count,
        'success': True
    })


# Serve the main HTML file
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')


# Serve static files (CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)