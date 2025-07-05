# utils.py (Gemini version)

import os
import google.generativeai as genai
from textblob import TextBlob

# Load API key securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt, model_name="gemini-pro"):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {str(e)}"

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "😊 Positive"
    elif polarity < -0.3:
        return "😟 Negative"
    else:
        return "😐 Neutral"
