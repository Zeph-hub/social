from transformers import pipeline
from langdetect import detect

sentiment_model = None


def get_sentiment_model():
    global sentiment_model
    if sentiment_model is None:
        sentiment_model = pipeline("sentiment-analysis")
    return sentiment_model


def analyze_text(text):
    try:
        lang = detect(text)
    except Exception:
        lang = "unknown"
    classifier = get_sentiment_model()
    sentiment = classifier(text[:512])[0]["label"]
    return lang, sentiment
