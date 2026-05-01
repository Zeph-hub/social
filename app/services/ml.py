from transformers import pipeline
from langdetect import detect

sentiment_model = pipeline("sentiment-analysis")

def analyze_text(text):
    try:
        lang = detect(text)
    except:
        lang = "unknown"
    sentiment = sentiment_model(text[:512])[0]["label"]
    return lang, sentiment
