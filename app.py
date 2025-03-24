import streamlit as st
import json
import os
from datetime import datetime
from api import (
    fetch_news,
    analyze_sentiment,
    generate_comparative_analysis,
    text_to_speech_hindi,
    translate_to_hindi,
    generate_overall_summary
)
from utils import (
    clean_text,
    truncate_text,
    save_to_json,
    get_cached_data,
    create_cache_dir
)

# Page configuration
st.set_page_config(
    page_title="News Summarization and Text-to-Speech Application",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add some CSS styling
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .report-section {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
    .article-title {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .article-source {
        color: #6c757d;
        font-style: italic;
    }
    .stExpander {
        border: 1px solid #f0f0f0;
    }
    h1, h2, h3 {
        margin-bottom: 1rem;
    }
    .summary-box {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .topic-tag {
        background-color: #e7f5ff;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        margin-right: 0.5rem;
        display: inline-block;
    }
    .comparison-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #007bff;
    }
    .impact-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #28a745;
    }
    .overlap-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("News Summarization and Text-to-Speech Application")
st.markdown("""
This app scans news articles about a custom company, 
offering sentiment analysis, identifying key topics, 
and delivering an insightful summary with text-to-speech in Hindi.
""")

# Main header area
st.header("Application Configuration")

# Custom company input
custom_company = st.text_input("Enter the company name:", placeholder="e.g., Tesla", key="custom_company_input")

# Number of articles to analyze
num_articles = st.number_input("Number of articles to analyze:", min_value=1, max_value=100, value=10)

# Cache option
use_cache = st.checkbox("Use cached data", value=True)



# Progress view holder
progress_placeholder = st.empty()

# Main function to analyze news
def analyze_company_news(company_name, num_articles, use_cache):
    """
    Analyze news for the given company
    """
    # Check if cached data is available
    if use_cache:
        cached_data = get_cached_data(company_name)
        if cached_data and len(cached_data.get('articles', [])) >= num_articles:
            st.success(f"Using cached data for {company_name} from {cached_data.get('timestamp', 'recent')}!")
            return cached_data.get('articles', [])[:num_articles]
    
    # Display progress
    progress_bar = progress_placeholder.progress(0)
    progress_text = progress_placeholder.empty()
    
    # Fetch news data
    progress_text.text("Fetching news articles...")
    news_data = fetch_news(company_name, num_articles)
    progress_bar.progress(50)
    
    # Update progress
    progress_text.text("Analyzing content and generating summaries...")
    progress_bar.progress(100)
    
    # Clear progress indicators
    progress_bar.empty()
    progress_text.empty()
    
    # Cache the results
    cache_dir = create_cache_dir()
    cache_data = {
        'company': company_name,
        'articles': news_data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_to_json(cache_data, os.path.join(cache_dir, f"{company_name.lower().replace(' ', '')}.json"))
    
    return news_data

# Generate a play button for audio
def get_audio_button(text, language="en", button_text="Listen"):
    audio_file = text_to_speech_hindi(text) if language == "hi" else None
    if audio_file:
        return st.audio(audio_file, format="audio/mp3")
    return None

# Analysis button
if st.button("Analyze Custom Company News"):
    if not custom_company:
        st.error("Please enter a custom company name")
    else:
        # Fetch and analyze news
        news_data = analyze_company_news(custom_company, 10, use_cache)
        
        if news_data:
            # Generate comparative analysis
            comparative_analysis = generate_comparative_analysis(news_data)
            
            # Generate overall summary
            overall_summary = generate_overall_summary(custom_company, news_data, comparative_analysis)
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Analysis Dashboard", "JSON Output"])
            
            with tab1:


                # Sentiment Distribution
                st.subheader("Sentiment Distribution")
                
                # Create columns for the sentiment counts
                col1, col2, col3 = st.columns(3)
                
                sentiment_counts = comparative_analysis['sentiment_counts']
                with col1:
                    st.metric(
                        label="Positive",
                        value=sentiment_counts['Positive'],
                        delta=f"{(sentiment_counts['Positive']/len(news_data)*100):.0f}%"
                    )
                
                with col2:
                    st.metric(
                        label="Neutral",
                        value=sentiment_counts['Neutral'],
                        delta=f"{(sentiment_counts['Neutral']/len(news_data)*100):.0f}%"
                    )
                
                with col3:
                    st.metric(
                        label="Negative",
                        value=sentiment_counts['Negative'],
                        delta=f"{(sentiment_counts['Negative']/len(news_data)*100):.0f}%"
                    )
                
                # Average sentiment
                avg_score = comparative_analysis['average_sentiment_score']
                sentiment_class = "sentiment-positive" if avg_score > 0.1 else ("sentiment-negative" if avg_score < -0.1 else "sentiment-neutral")
                sentiment_label = "Positive" if avg_score > 0.1 else ("Negative" if avg_score < -0.1 else "Neutral")
                
                st.markdown(f"<p>Average Sentiment: <span class='{sentiment_class}'>{sentiment_label} ({avg_score:.2f})</span></p>", unsafe_allow_html=True)
                
                # Topic Overlap Section
                st.subheader("Topic Analysis")
                
                # Common Topics
                st.markdown("#### Common Topics Across Articles")
                common_topics = comparative_analysis['topic_overlap']['Common Topics']
                
                if common_topics:
                    topics_html = ""
                    for topic in common_topics:
                        topics_html += f"<span class='topic-tag'>{topic}</span>"
                    st.markdown(f"<div class='overlap-box'>{topics_html}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("No common topics found across all articles.")
                
                # Most Frequent Topics
                st.markdown("#### Most Frequent Topics")
                topics_html = ""
                for topic, count in comparative_analysis['common_topics'][:8]:
                    topics_html += f"<span class='topic-tag'>{topic} ({count})</span>"
                
                st.markdown(f"<div>{topics_html}</div>", unsafe_allow_html=True)
                
                # Unique Topics by Article
                st.markdown("#### Unique Topics by Article")
                unique_topics = comparative_analysis['unique_topics_by_article']
                
                if unique_topics:
                    for unique in unique_topics:
                        st.markdown(f"{unique['Title']}: " + ", ".join(unique['Unique Topics']))
                else:
                    st.markdown("No unique topics identified.")
                
                # Coverage Differences
                st.subheader("Coverage Differences")
                if comparative_analysis['coverage_differences']:
                    for diff in comparative_analysis['coverage_differences']:
                        st.markdown(f"<div class='comparison-box'><strong>Comparison:</strong> {diff['Comparison']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='impact-box'><strong>Impact:</strong> {diff['Impact']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("No significant coverage differences identified.")
                
                # Individual Articles
                st.header("📄 Individual Articles Analysis")
                
                # Create tabs
                tab_labels = [f"Article {i+1}" for i in range(len(news_data))]
                article_tabs = st.tabs(tab_labels)
                
                for i, (tab, article) in enumerate(zip(article_tabs, news_data)):
                    with tab:
                        # Article header
                        st.markdown(f"<h3 class='article-title'>{article['title']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p class='article-source'>Source: {article['source']} | Date: {article['date']} | Reading time: {article['reading_time']}</p>", unsafe_allow_html=True)
                        
                        # Summary and sentiment
                        st.markdown("### Summary")
                        # Removed Hindi article summary translation



                        # st.markdown(hindi_article_summary)


                        sentiment = article['sentiment']
                        sentiment_class = "sentiment-positive" if sentiment['label'] == "Positive" else ("sentiment-negative" if sentiment['label'] == "Negative" else "sentiment-neutral")
                        
                        st.markdown(f"### Sentiment: <span class='{sentiment_class}'>{sentiment['label']} ({sentiment['score']:.2f})</span>", unsafe_allow_html=True)
                        
                        # Topics
                        st.markdown("### Topics")
                        topics_html = ""
                        for topic in article['topics']:
                            topics_html += f"<span class='topic-tag'>{topic}</span>"
                        st.markdown(f"<div>{topics_html}</div>", unsafe_allow_html=True)
                        
                        # Full content in expander
                        with st.expander("View Full Article Content"):
                            st.markdown(article['content'])
                            st.markdown(f"[Read original article]({article['url']})")
                
                # Final Sentiment Analysis
                st.header("🎯 Final Sentiment Analysis")
                st.markdown(f"<div class='summary-box'>{comparative_analysis['final_sentiment_analysis']}</div>", unsafe_allow_html=True)
                
                # Hindi Audio summary
                st.header("🔊 Audio Summary (Hindi)")
                
                # Translate summary to Hindi
                hindi_summary = translate_to_hindi(overall_summary)
                
                # Display Hindi text
                with st.expander("View Hindi Text"):
                    st.text(hindi_summary)
                
                # Generate and play audio
                with st.spinner("Generating Hindi audio..."):
                    audio_file = text_to_speech_hindi(hindi_summary)
                    st.audio(audio_file, format="audio/mp3")
                
                # Export options
                st.header("📥 Export Results")
                
                # Audio download
                st.download_button(
                    label="Download Audio Summary (Hindi)",
                    data=audio_file,
                    file_name=f"{custom_company}_summary_hindi.mp3",
                    mime="audio/mp3"
                )
            
            with tab2:
                # JSON Output View
                st.header("JSON Output Format")
                
                # Prepare JSON data
                json_data = {
                    "Company": custom_company,
                    "Articles": [
                        {
                            "Title": article['title'],
                            "Summary": article['summary'],
                            "Sentiment": article['sentiment']['label'],
                            "Topics": article['topics']
                        } for article in news_data
                    ],
                    "Comparative Sentiment Score": {
                        "Sentiment Distribution": comparative_analysis['sentiment_counts'],
                        "Coverage Differences": comparative_analysis['coverage_differences'],
                        "Topic Overlap": {
                            "Common Topics": comparative_analysis['topic_overlap']['Common Topics'],
                            "Most Frequent Topics": comparative_analysis['common_topics']
                        }
                    },
                    "Final Sentiment Analysis": comparative_analysis['final_sentiment_analysis'],
                    "Audio": "[Play Hindi Speech]"
                }
                
                # Display JSON
                st.json(json_data)
                
                # JSON download
                json_str = json.dumps(json_data, indent=2)
                
                st.download_button(
                    label="Download Analysis Report (JSON)",
                    data=json_str,
                    file_name=f"{custom_company}_analysis.json",
                    mime="application/json"
                )
        else:
            st.error("Failed to fetch news data. Please try again later or with a different company name.")

# Instructions at the bottom
st.markdown("---")
st.markdown("### How to Use")
st.markdown("""
1. Enter a custom company name.
2. Adjust the number of articles to analyze if needed.
3. Click the "Analyze Custom Company News" button to start the analysis.
4. Explore the sentiment analysis, topics, and individual article details.
5. Listen to the Hindi audio summary or download the results.
6. View and download the JSON output.
""")

# Footer
st.markdown("---")
st.markdown("Built for Akaike Internship Assignment | News Summarization and Text-to-Speech Application")
st.markdown("Created By Ganesh Patel")
