# News Article Summarizer

A Python tool that automatically generates concise summaries of news articles using natural language processing techniques.

## Features

- Summarize news articles from various sources:
  - URLs (web articles)
  - Text files
  - Direct text input
- Customize summary length by specifying the number of sentences
- Extract the most important information using NLP algorithms
- Save summaries to files for future reference

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/navi-siddu-1103/news-summarizer.git
   cd news-summarizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. The tool will automatically download required NLTK resources on first run.

## Usage

### Summarize an article from a URL:

```
python news_summarizer.py -u https://example.com/news-article -n 5 -o summary.txt
```

### Summarize an article from a text file:

```
python news_summarizer.py -f example_articles/sample_article1.txt -n 3 -o summary.txt
```

### Summarize text directly:

```
python news_summarizer.py -t "This is the article text that you want to summarize..." -n 4 -o summary.txt
```

### Command-line Arguments:

- `-u, --url`: URL of the news article to summarize
- `-f, --file`: Path to a text file containing the news article
- `-t, --text`: Direct text input to summarize
- `-n, --num-sentences`: Number of sentences to include in the summary (default: 5)
- `-o, --output`: Output file name (default: summary.txt)

## How It Works

The summarizer uses extractive summarization techniques:

1. **Preprocessing**: Tokenizes the article into sentences and words
2. **Filtering**: Removes stopwords and non-alphabetic words
3. **Scoring**: Calculates word frequencies and scores sentences based on important words
4. **Selection**: Selects the highest-scoring sentences to form the summary
5. **Presentation**: Outputs the summary in the original sentence order

## Limitations

- The summarizer is extractive, not abstractive (it selects existing sentences rather than generating new ones)
- Web scraping may not work perfectly on all news sites due to varying page structures
- Performance depends on the quality and structure of the input text

## Future Improvements

- Add support for multiple languages
- Implement abstractive summarization using transformer models
- Create a simple web interface
- Add more preprocessing options for better quality

## License

This project is licensed under the MIT License - see the LICENSE file for details.
