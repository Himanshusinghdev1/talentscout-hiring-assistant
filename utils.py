# utils.py

import openai
import os
from textblob import TextBlob

# Load API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt, temperature=0.7, model="gpt-4"):
    """
    Sends a prompt to OpenAI's ChatCompletion API and returns the response text.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Error from OpenAI API: {str(e)}"

def analyze_sentiment(text):
    """
    Analyzes sentiment of a given text and returns a labeled emoji.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        return "😊 Positive"
    elif polarity < -0.3:
        return "😟 Negative"
    else:
        return "😐 Neutral"
