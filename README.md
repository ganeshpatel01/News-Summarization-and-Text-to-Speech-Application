News Sentiment Analysis and Text-to-Speech Application
This web application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.
Features

News Extraction: Extracts news articles from various sources using BeautifulSoup
Sentiment Analysis: Analyzes article content sentiment (positive, negative, neutral)
Comparative Analysis: Compares sentiment across multiple articles
Topic Extraction: Identifies key topics from each article
Hindi Text-to-Speech: Converts summarized content to Hindi speech
User-friendly Interface: Simple Streamlit web interface
Downloadable Results: Export analysis as JSON and audio as WAV

Demo
The application is deployed on Hugging Face Spaces and can be accessed here: [Hugging Face Deployment Link](https://huggingface.co/spaces/Ganesh3560/News_TTS_)

Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ganeshpatel01/News-Summarization-and-Text-to-Speech-Application
   cd News-Summarization-and-Text-to-Speech-Application
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download NLTK data (this will be done automatically on the first run, but can be done manually):
   ```python
   import nltk
   nltk.download('punkt')
   ```

### Running the Application
- Start the Streamlit app:
  ```bash
  streamlit run app.py
  ```
- Open your web browser and navigate to [http://localhost:8501](http://localhost:8501)

### How to Work with the Application
1. **Enter a Company Name**: In the input field, type the name of the company you want to analyze (e.g., "Tesla").
2. **Set the Number of Articles**: Use the number input to specify how many articles you want to analyze (default is 10).
3. **Use Cached Data**: If you want to use previously fetched data, check the "Use cached data" box.
4. **Start Analysis**: Click the "Analyze Custom Company News" button to begin the analysis.
5. **View Results**: After the analysis is complete, you will see:
   - **Sentiment Distribution**: A breakdown of positive, neutral, and negative sentiments.
   - **Topic Analysis**: Common and unique topics identified in the articles.
   - **Individual Articles**: Detailed analysis of each article, including sentiment and topics.
6. **Listen to Audio Summary**: You can listen to the Hindi audio summary generated from the analysis.
7. **Download Results**: Options to download the audio summary and the analysis report in JSON format are available.

API Reference
The application consists of several components:
app.py
The main Streamlit application that handles the user interface.
api.py
Contains the backend functionality:

fetch_news(company_name, num_articles=10): Fetches news articles
analyze_sentiment(text): Performs sentiment analysis
extract_topics(text, company_name): Extracts key topics
generate_comparative_analysis(articles): Conducts comparative analysis
text_to_speech_hindi(text): Converts text to Hindi speech

utils.py
Contains utility functions:

clean_text(text): Cleans and normalizes text
format_date(date_str): Standardizes date formats
generate_cache_key(company_name): Creates cache keys
calculate_reading_time(text): Estimates reading time
truncate_text(text, max_length=100): Truncates text with ellipsis

Project Structure
news-sentiment-tts/
├── app.py                # Main Streamlit application
├── api.py                # API functions
├── utils.py              # Utility functions
├── requirements.txt      # Dependencies
├── README.md             # Documentation
└── .gitignore            # Git ignore file
Deployment
Hugging Face Spaces

Create a new Space on Hugging Face
Connect your GitHub repository
Set the Space SDK to "Streamlit"
The app will be automatically deployed

Limitations

The news extraction may be affected by website changes or anti-scraping measures
Sentiment analysis is performed using a pre-trained model and may not perfectly capture nuanced sentiments
The application uses a simple approach for topic extraction which may not always identify the most relevant topics
Hindi TTS uses gTTS which requires an internet connection

Future Improvements

Implement caching to reduce API calls and improve performance
Add more sophisticated topic modeling using LDA or other techniques
Improve the sentiment analysis with fine-tuned models
Add support for more languages
Implement a more robust scraping mechanism

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Streamlit for the web application framework
Hugging Face Transformers for NLP models
gTTS for Text-to-Speech functionality
BeautifulSoup for web scraping
