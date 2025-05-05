# sentiment.py
from transformers import pipeline

# Load transformer sentiment model (Hugging Face)
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(texts: list[str]) -> list[str]:
    results = sentiment_model(texts)
    return [r['label'] for r in results]
