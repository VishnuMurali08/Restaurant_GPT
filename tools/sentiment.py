import pandas as pd
import os
from dotenv import load_dotenv
from data.db import fetch_table
from openai import OpenAI

# Load environment and API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔍 Classify sentiment of a review
def analyze_sentiment(text):
    prompt = f"Classify the following review as Positive, Negative, or Neutral:\nReview: \"{text}\"\nSentiment:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

# 🧭 Extract complaint theme from a review
def extract_complaint_theme(text):
    prompt = (
        "Extract the main complaint theme from the following review. "
        "Choose from: 'Service', 'Food Quality', 'Waiting Time', 'Price', or 'None'.\n"
        f"Review: \"{text}\"\nTheme:"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

# 🔁 Annotate all reviews with sentiment and complaint theme
def process_reviews(source=None):
    df = fetch_table("reviews")
    if source:
        df = df[df["source"] == source]

    df["sentiment"] = df["review_text"].apply(analyze_sentiment)
    df["complaint_theme"] = df["review_text"].apply(extract_complaint_theme)
    return df

# 📊 Summarize overall sentiment and complaint themes
def summarize_sentiment_trends(_=None):
    df = process_reviews()
    output = ""

    # Overall counts
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

    # By source
    for source in df["source"].unique():
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

# 🧵 Summarize all reviews for a specific complaint theme
def summarize_specific_complaints(theme="Service"):
    df = process_reviews()
    theme = theme.strip().title()

    # Handle 'None' explicitly
    if theme.lower() == "none":
        return "👍 No major complaints were flagged in these reviews. Customers seem generally satisfied!"

    # Filter reviews matching the theme
    filtered_df = df[df["complaint_theme"].str.lower() == theme.lower()]

    if filtered_df.empty:
        return f"✅ No complaints related to **{theme}** were found in the current review set."

    # Combine relevant reviews
    review_texts = "\n".join(
        f"- {row['review_date']}: {row['review_text']} ({row['source']})"
        for _, row in filtered_df.iterrows()
    )

    # Prompt GPT to summarize the actual complaints
    prompt = f"""
You're a helpful assistant analyzing restaurant reviews. A user asked about customer complaints related to **{theme}**.

Here are real reviews tagged under that theme:

{review_texts}

Please:
- Summarize the common issues mentioned
- Use a friendly, clear, and helpful tone
- Group similar complaints
- Rephrase issues naturally, avoid quoting unless useful
- Format your response with bullet points or short paragraphs

Summary:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
