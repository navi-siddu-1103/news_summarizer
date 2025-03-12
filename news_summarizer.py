# news_summarizer.py

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest
import re
import argparse

# Download required NLTK resources
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading required NLTK resources...")
        nltk.download('punkt')
        nltk.download('stopwords')

# Function to fetch article content from URL
def fetch_article(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Find the main text content (this varies by website)
        # This is a simple approach that may need customization for specific sites
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        # Clean the text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
        text = re.sub(r'\n', ' ', text)   # Replace newlines with space
        
        return text
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None

# Summarize text using extractive summarization
def summarize_text(text, num_sentences=5):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Filter out stopwords and non-alphabetic words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Calculate word frequencies
    word_frequencies = FreqDist(filtered_words)
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if i not in sentence_scores:
                    sentence_scores[i] = word_frequencies[word]
                else:
                    sentence_scores[i] += word_frequencies[word]
    
    # Get the most important sentences
    summary_sentences_indices = nlargest(min(num_sentences, len(sentences)), 
                                        sentence_scores, key=sentence_scores.get)
    summary_sentences_indices.sort()  # Sort to maintain original order
    
    # Create the summary
    summary = [sentences[i] for i in summary_sentences_indices]
    
    return ' '.join(summary)

# Function to save summary to a file
def save_summary(summary, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Summary saved to {output_file}")

# Function to read text from file
def read_article_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Main function
def main():
    parser = argparse.ArgumentParser(description='Summarize news articles')
    
    # Create a mutually exclusive group for input source
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-u', '--url', help='URL of the news article to summarize')
    input_group.add_argument('-f', '--file', help='Path to a text file containing the news article')
    input_group.add_argument('-t', '--text', help='Direct text input to summarize')
    
    # Other arguments
    parser.add_argument('-n', '--num-sentences', type=int, default=5, 
                        help='Number of sentences in the summary (default: 5)')
    parser.add_argument('-o', '--output', default='summary.txt',
                        help='Output file name (default: summary.txt)')
    
    args = parser.parse_args()
    
    # Download NLTK resources if needed
    download_nltk_resources()
    
    # Get the article text based on the input source
    if args.url:
        print(f"Fetching article from URL: {args.url}")
        article_text = fetch_article(args.url)
    elif args.file:
        print(f"Reading article from file: {args.file}")
        article_text = read_article_from_file(args.file)
    else:  # args.text
        article_text = args.text
    
    if not article_text:
        print("Failed to obtain article text. Exiting.")
        return
    
    # Generate the summary
    print(f"Generating summary with {args.num_sentences} sentences...")
    summary = summarize_text(article_text, args.num_sentences)
    
    # Save and display summary
    save_summary(summary, args.output)
    
    print("\nSummary:")
    print("=" * 50)
    print(summary)
    print("=" * 50)

if __name__ == "__main__":
    main()