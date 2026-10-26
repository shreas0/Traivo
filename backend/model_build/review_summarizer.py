from PIL.ImagePalette import negative
import pandas as pd
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

positive_df=pd.read_csv('positive_reviews.csv')
negative_df=pd.read_csv('negative_reviews.csv')

api = os.getenv("GROQ_API_KEY")

if not api:
    raise ValueError("GROQ_API_KEY not found in your .env file")

client = Groq(api_key=api)


def summarized_positive(destination):
    destination = destination.strip()

    reviews = positive_df[
        positive_df["destination"].astype(str).str.strip().str.casefold()
        == destination.casefold()
    ]["review_text"].dropna().astype(str)

    if reviews.empty:
        return f"No positive reviews found for {destination}."


    pos_reviews = "\n".join(reviews)[:6000]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize positive travel reviews using only the supplied evidence. "
                    "Write a detailed, well-structured summary covering recurring "
                    "positive experiences, staff service, cleanliness, facilities, "
                    "location, food, and value for money when mentioned in the reviews. "
                    "Use headings and bullet points where appropriate. "
                    "Do not invent facts. Finish every sentence completely."
                )                   
            },
            {
                "role": "user",
                "content": (
                    f"Destination: {destination}\n\n"
                    f"Positive reviews:\n{pos_reviews}\n\n"
                    "Write a concise summary of what visitors liked."
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=600
    )

    return response.choices[0].message.content


def summarized_negative(destination):
    destination = destination.strip()

    reviews = negative_df[
        negative_df["destination"].astype(str).str.strip().str.casefold()
        == destination.casefold()
    ]["review_text"].dropna().astype(str)

    if reviews.empty:
        return f"No negative reviews found for {destination}."

    neg_reviews = "\n".join(reviews)[:6000]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize negative travel reviews using only the supplied evidence. "
                    "Write a detailed, well-structured summary covering recurring "
                    "complaints about staff service, cleanliness, facilities, "
                    "location, food, pricing, and maintenance when mentioned. "
                    "Use headings and bullet points where appropriate. "
                    "Do not invent facts. Finish every sentence completely."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Destination: {destination}\n\n"
                    f"Negative reviews:\n{neg_reviews}\n\n"
                    "Summarize the main complaints and recurring problems."
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=600
    )

    return response.choices[0].message.content



destination= input("enter : ")
print('\n',  "Positive Reviews : ", '\n' , summarized_positive(destination))
print('\n' , "Negative Reviews : ", '\n' , summarized_negative(destination))