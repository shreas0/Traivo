
import pandas as pd
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

positive_df = pd.read_csv('model_build/positive_reviews.csv')
negative_df = pd.read_csv('model_build/negative_reviews.csv')

api = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api)


def summarized_positive(destination):
    reviews = positive_df[positive_df["destination"].str.lower() == destination.lower()]["review_text"]
    if reviews.empty:
        return f"No positive reviews found for {destination}."

    pos_reviews = "\n".join(reviews)[:1200]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Briefly summarize the main positive points in the reviews. "
                    "Use only the supplied evidence and do not invent facts."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Destination: {destination}\n\n"
                    f"Positive reviews:\n{pos_reviews}\n\n"
                    "Keep it to at most 3 short bullets."
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=250
    )

    return response.choices[0].message.content


def summarized_negative(destination):
    reviews = negative_df[negative_df["destination"].str.lower() == destination.lower()]["review_text"]

    if reviews.empty:
        return f"No negative reviews found for {destination}."

    neg_reviews = "\n".join(reviews)[:1200]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Briefly summarize the main complaints in the reviews. "
                    "Use only the supplied evidence and do not invent facts."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Destination: {destination}\n\n"
                    f"Negative reviews:\n{neg_reviews}\n\n"
                    "Keep it to at most 3 short bullets."
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=250
    )

    return response.choices[0].message.content
