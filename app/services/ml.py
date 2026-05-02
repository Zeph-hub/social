import logging
from transformers import pipeline
from langdetect import detect

logger = logging.getLogger(__name__)
sentiment_model = None


def get_sentiment_model():
    global sentiment_model
    if sentiment_model is None:
        sentiment_model = pipeline("sentiment-analysis")
    return sentiment_model


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception as exc:
        logger.debug("Language detection failed: %s", exc)
        return "unknown"


def predict_sentiment(text: str) -> str:
    try:
        classifier = get_sentiment_model()
        return classifier(text[:512])[0]["label"]
    except Exception as exc:
        logger.debug("Sentiment classification failed: %s", exc)
        return "unknown"


def analyze_text(text: str):
    lang = detect_language(text)
    sentiment = predict_sentiment(text)
    return lang, sentiment
