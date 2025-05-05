# sentiment.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import numpy as np

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Define sentiment labels
labels_map = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}

# Pipeline version (simple and fast for batches)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=False)

def analyze_sentiment(texts: list[str]) -> list[str]:
    """
    Analyze a list of news headlines and return sentiment labels.

    Args:
        texts: List of strings (headlines)

    Returns:
        List of sentiment labels: "NEGATIVE", "NEUTRAL", "POSITIVE"
    """
    cleaned_texts = [text.replace("\n", " ").strip()[:512] for text in texts]  # Trim to 512 tokens
    results = classifier(cleaned_texts)
    return [r["label"].upper() for r in results]
