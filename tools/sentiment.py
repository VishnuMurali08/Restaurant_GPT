import pandas as pd
import os
from dotenv import load_dotenv
from data.db import fetch_table
from openai import OpenAI

# Load environment and set API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔍 Analyze overall sentiment of a review
def analyze_sentiment(text):
    prompt = f"Classify the following review as Positive, Negative, or Neutral:\nReview: \"{text}\"\nSentiment:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

# 🧭 Extract main complaint theme
def extract_complaint_theme(text):
    prompt = f"Extract the main complaint theme from the following review. Choose from: 'Service', 'Food Quality', 'Waiting Time', 'Price', or 'None'.\nReview: \"{text}\"\nTheme:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

# 🔁 Analyze all reviews (or optionally filter by source)
def process_reviews(source=None):
    df = fetch_table("reviews")
    if source:
        df = df[df["source"] == source]

    df["sentiment"] = df["review_text"].apply(analyze_sentiment)
    df["complaint_theme"] = df["review_text"].apply(extract_complaint_theme)
    return df

# 📊 Summarize sentiment trends across all reviews or for a specific source
def summarize_sentiment_trends(_=None):
    df = process_reviews()  # Load all reviews
    output = ""

    # === Overall Summary ===
    overall_sentiment = df["sentiment"].value_counts().to_dict()
    overall_complaints = df["complaint_theme"].value_counts().to_dict()

    output += "\U0001f4ca **Overall Sentiment Summary:**\n"
    for sentiment, count in overall_sentiment.items():
        output += f"- {sentiment}: {count} reviews\n"

    output += "\n\u26a0\ufe0f **Overall Complaint Themes:**\n"
    for theme, count in overall_complaints.items():
        if theme != "None":
            output += f"- {theme}: {count} mentions\n"

    output += "\n" + ("=" * 50) + "\n"

    # === Grouped by Source ===
    sources = df["source"].unique()

    for source in sources:
        source_df = df[df["source"] == source]
        sentiment_summary = source_df["sentiment"].value_counts().to_dict()
        complaint_summary = source_df["complaint_theme"].value_counts().to_dict()

        output += f"\n\U0001f4ca **Sentiment Summary from {source}:**\n"
        for sentiment, count in sentiment_summary.items():
            output += f"- {sentiment}: {count} reviews\n"

        output += "\n\u26a0\ufe0f **Complaint Themes:**\n"
        for theme, count in complaint_summary.items():
            if theme != "None":
                output += f"- {theme}: {count} mentions\n"
        output += "\n" + ("-" * 50) + "\n"

    return output.strip()
