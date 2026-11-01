from pyexpat.errors import messages
import os
import json
import ast
import re
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from dotenv import load_dotenv

load_dotenv(override=True)

import model_build.main_model as mm
import model_build.review_summarizer as rs
import model_build.budget_model as bm
import model_build.attraction_model as am
from features.google_maps import google_maps_link
from groq import Groq

api = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api)

def user_input_organizer(message, history=None):
    history = history or []
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages = [{
        "role": "system",
        "content": (
            "u need to analyze the user message text"
            "Extract the informations from the message related to these only : budget_preference, group_preference, vibe_preference,climate_preference, continent_preference"
            "u are a travel preference extraction bot."
            "extract exactly 5 preferences in this order:1. budget_preference2. group_preference3. vibe_preference4. climate_preference5. continent_preference"
            "rules:- match the user's meaning to the closest allowed value.- ignore capitalization and minor spelling mistakes.- use only the allowed values.- if a preference is missing or unclear, use 'any'.- don't guess or invent preferences.- retain earlier preferences unless the user changes them.- return only a python-style list containing exactly 5 strings.- don't include explanations or markdown."
            "budget_preference:['budget', 'mid-range', 'premium', 'any']"
            "group_preference:['couples', 'friends', 'family', 'solo', 'any']"
            "vibe_preference:['beach nightlife', 'adventure nature', 'culture heritage','romantic lakeside', 'nature relaxation', 'adventure wellness','spiritual culture', 'heritage sightseeing', 'hill station relaxation','scenic tea culture', 'nature hill station', 'island beach adventure','coastal heritage cafes', 'urban food nightlife', 'urban heritage food','tea hills nature', 'desert culture adventure', 'lakes mountains romance','urban cafes culture', 'high altitude adventure', 'urban food attractions','beach wellness culture', 'culture trekking', 'coastal city culture','urban food shopping', 'luxury shopping attractions', 'heritage food city','art romance food', 'history food architecture', 'beach art nightlife','urban museums theatre', 'canals art cycling', 'heritage walkable','coastal culture food', 'urban arts food', 'nature city outdoors','food history art', 'beach resort nightlife', 'coastal mountains food','markets heritage desert', 'island beach culture', 'history urban culture','coastal city outdoors', 'adventure lakes mountains','urban food technology', 'heritage gardens culture','urban food pop culture', 'island beach water sports','street food heritage', 'nature northern lights', 'heritage trekking','beach music nightlife', 'culture food architecture','mountain lakes outdoors', 'any']"
            "climate_preference:['tropical', 'mountain', 'semi-arid', 'subtropical','humid subtropical', 'arid desert', 'temperate','tropical wet-dry', 'cold desert', 'subtropical highland','Mediterranean', 'oceanic', 'continental', 'humid continental','tropical monsoon', 'subpolar oceanic', 'tropical savanna','subarctic', 'any']"
            "continent_preference:['Asia', 'Europe/Asia', 'Europe', 'North America','Africa', 'Oceania', 'South America', 'Asia/Europe', 'any']"
            "examples:user: i want a cheap beach trip with my friends in africaoutput: ['budget', 'friends', 'beach nightlife', 'any', 'Africa']user: i want a luxury mountain trip with my partneroutput: ['premium', 'couples', 'nature hill station', 'mountain', 'any']user: suggest somewhere affordableoutput: ['budget', 'any', 'any', 'any', 'any']"
        )},
        *history,
        {
            "role": "user",
            "content": "Analyze this latest message using the conversation for context. Return the output as a Python list:\n\n" + message
        }],

        temperature=0.2,
        max_completion_tokens=300,
        reasoning_effort="low"
    )


    input_list = response.choices[0].message.content or ""
    try:
        preferences = ast.literal_eval(input_list.strip().replace("```python", "").replace("```", ""))
        if isinstance(preferences, list) and len(preferences) == 5:
            return preferences
    except (ValueError, SyntaxError):
        pass
    return ["any", "any", "any", "any", "any"]
    


def model_response(message_data, selected_destinations=None):
    destination = selected_destinations or mm.model_response(
        message_data[0], message_data[1], message_data[2], message_data[3], message_data[4]
    )
    result={}
    for s in destination:
        reviews={"positive" : rs.summarized_positive(s) , "negative" : rs.summarized_negative(s) }

        result[s]=reviews

    

    return result


def destinations_in_text(message):
    destinations = mm.data["destination_name"].dropna().unique()
    found = []
    for destination in sorted(destinations, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(destination.lower()) + r"(?!\w)"
        if re.search(pattern, message.lower()) and not any(
            destination.lower() in place.lower() for place in found
        ):
            found.append(destination)
        if len(found) == 3:
            break
    return found


def budget_for_message(message, history=None):
    budget_words = ["budget", "cost", "costs", "expensive", "cheap", "afford", "affordable", "price", "how much", "estimate", "estimated", "spend"]
    if not any(word in message.lower() for word in budget_words):
        return ""

    places = destinations_in_text(message)
    if not places:
        for item in reversed(history or []):
            if isinstance(item, dict) and isinstance(item.get("content"), str):
                places = destinations_in_text(item["content"])
                if places:
                    break
    if not places:
        return ""

    details = {
        "destination": places[0], "travellers": 1, "trip_days": 3,
        "travel_style": "comfortable", "season_demand": "low",
        "activity_intensity": "balanced", "accommodation_type": "midrange_hotel",
        "trip_origin_type": "same_country",
    }
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract trip details for a rough travel budget estimate. "
                        "Return only valid JSON with destination, travellers, trip_days, travel_style, "
                        "season_demand, activity_intensity, accommodation_type, trip_origin_type. "
                        "Use the destination supplied by the user. Use numbers for travellers and trip_days. "
                        "Allowed travel_style: budget, comfortable, luxury, standard. season_demand: low, shoulder, peak. "
                        "activity_intensity: relaxed, balanced, packed. accommodation_type: hostel, budget_hotel, "
                        "midrange_hotel, premium_hotel. trip_origin_type: same_country, international. "
                        "If not specified, use 1 traveller, 3 days, midrange, low, balanced, midrange_hotel, same_country."
                    ),
                },
                {"role": "user", "content": (
                    "Conversation: " + json.dumps((history or [])[-8:], ensure_ascii=False)
                    + "\nLatest message: " + message
                    + "\nDestination detected: " + places[0]
                )},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_completion_tokens=200,
            reasoning_effort="low",
        )
        extracted_details = json.loads(response.choices[0].message.content or "{}")
        if isinstance(extracted_details, dict):
            details.update(extracted_details)
        if details.get("travel_style") == "midrange":
            details["travel_style"] = "comfortable"
        details["destination"] = places[0]
    except Exception:
        pass

    estimate = bm.predict_budget(details)
    travellers = int(details.get("travellers") or 1)
    days = int(details.get("trip_days") or 3)
    return (
        f"Budget model estimate for {places[0]}: about ₹{estimate:,} total for "
        f"{travellers} traveller(s) over {days} days. This is a rough estimate based on the supplied trip details."
    )


def attractions_for_message(message, history=None):
    history = history or []
    attraction_words = ["attraction", "things to do", "places to visit", "sightseeing", "itinerary", "visit places", "suggest places", "recommend places", "what to do", "activities", "places", "tourist spot", "tourist place"]
    if not any(word in message.lower() for word in attraction_words):
        return ""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": (
                    "Analyze the latest travel request and conversation. Extract the destination, "
                    "interest (beach, nature, history, culture, adventure, food, or any), "
                    "budget (low, medium, high, or any), and available visit hours (2, 4, or 8). "
                    "Only give a destination explicitly mentioned or clearly established in context. "
                    "Return only JSON with keys destination, vibe, budget, hours. If no destination, use an empty string."
                )},
                *history[-8:],
                {"role": "user", "content": message},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_completion_tokens=150,
            reasoning_effort="low",
        )
        details = json.loads(response.choices[0].message.content or "{}")
        destination = str(details.get("destination", "")).strip()
        available_destinations = am.data["destination"].drop_duplicates().tolist()
        requested_destinations = destinations_in_text(message)
        if not requested_destinations:
            for item in reversed(history):
                if item.get("role") == "user":
                    requested_destinations = destinations_in_text(item.get("content", ""))
                    if requested_destinations:
                        break
        direct_destination = next(
            (place for place in requested_destinations
             if any(place.lower() == available.lower() for available in available_destinations)),
            "",
        )
        if direct_destination:
            destination = direct_destination
        if not destination:
            return ""

        matches = am.data[am.data["destination"].str.lower() == destination.lower()]
        if matches.empty:
            matches = am.data[am.data["destination"].str.lower().apply(
                lambda available: available in destination.lower() or destination.lower() in available
            )]
        if matches.empty:
            return ""
        destination = matches.iloc[0]["destination"]
        vibe = details.get("vibe", "any")
        if vibe not in ["any", "beach", "nature", "history", "culture", "adventure", "food"]:
            vibe = "any"
        budget = details.get("budget", "any")
        if budget not in ["any", "low", "medium", "high"]:
            budget = "any"
        try:
            hours = int(details.get("hours", 8))
        except (TypeError, ValueError):
            hours = 8
        if hours not in [2, 4, 8]:
            hours = 8

        attractions = am.recommend_attractions(destination, vibe, budget, hours)
        if not attractions:
            return ""
        links = "\n\nPlaces to consider in " + destination + ":\n" + "\n".join(
            f"- [{place}]({google_maps_link(place, destination)})" for place in attractions
        )
        return links
    except Exception:
        return ""


def analyze_image_request(user_input, response_text, history=None):
    conversation = [
        {"role": item["role"], "content": item["content"]}
        for item in (history or [])[-8:]
        if isinstance(item, dict)
        and item.get("role") in ["user", "assistant"]
        and isinstance(item.get("content"), str)
    ]
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages = [{
        "role": "system",
        "content": """
        decide whether images would make the assistant's response more useful and visually appealing.

        show images when the assistant recommends travel destinations, tourist attractions, hotels, restaurants, or traexperiences. images                    should also be shown when suggesting places to visit, creating itineraricomparing destinations, or sharing opinions about a place. if                    the user asks something like "whatyou think about goa?" or "is manali worth visiting?", images would help them get a better idea of                    place.

        also show images when describing the beauty, scenery, beaches, mountains, architecture, or overall atmosphere odestination, or                    whenever the user explicitly asks for photos.

        don't show images when the user is only asking about reviews, complaints, ratings, weather, prices, budget, distantimings,                    transportation, or booking details. the same applies to general questions, explanatiotravel policies, and casual conversations where                    images wouldn't really add anything.

        only select places that are actually mentioned in the assistant's response. choose the most relevant ones that wobenefit from having                    images. don't invent place names, include generic terms, or repeat the slocation. you can select up to 3 places.

        remember that images should complement the response, not just fill up space. don't show them simply because a destinatis mentioned.                    consider what the user is asking and whether seeing the place would genuinely imprtheir experience.

        return only valid json in this format:
        {
            "show_images": true,
            "places": ["Goa", "Baga Beach"]
        }

        if images aren't useful, return false with an empty places array. don't include markdown, explanations, or any additiokeys.
        """
    },
    {
        "role": "user",
        "content": (
            "conversation: " + json.dumps(conversation, ensure_ascii=False) +
            "\nlatest user request: " + user_input +
            "\nassistant response: " + response_text
        )
    }
],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_completion_tokens=200,
            reasoning_effort="low"
        )
        result = json.loads(response.choices[0].message.content or "{}")
        if result.get("show_images") is not True:
            return []
        return [
            place.strip()
            for place in result.get("places", [])
            if isinstance(place, str) and place.strip() and place.strip().lower() in response_text.lower()
        ][:3]
    except Exception:
        return []


def place_images_for_response(places, history=None):
    api_key = os.getenv("UNSPLASH_API")
    if not api_key:
        return []

    history = history or []
    previous_images = [
        image
        for message in history
        if isinstance(message, dict)
        for image in message.get("images", [])
        if isinstance(image, dict)
    ]
    previous_urls = [image.get("url") for image in previous_images]

    images = []
    for place in places:
        try:
            url = "https://api.unsplash.com/search/photos?query=" + quote_plus(place + " travel") + "&per_page=10&orientation=landscape"
            req = Request(url, headers={"Authorization": "Client-ID " + api_key, "Accept-Version": "v1"})
            with urlopen(req, timeout=5) as response:
                photos = json.load(response).get("results", [])
            photo = next((photo for photo in photos if photo["urls"]["regular"] not in previous_urls), None)
            if photo:
                images.append({
                    "place": place,
                    "url": photo["urls"]["regular"],
                    "alt": photo.get("alt_description") or place,
                    "photographer": photo["user"]["name"],
                    "photographer_url": photo["user"]["links"]["html"] + "?utm_source=traivo&utm_medium=referral",
                    "unsplash_url": "https://unsplash.com/?utm_source=traivo&utm_medium=referral"
                })
                previous_urls.append(photo["urls"]["regular"])
        except Exception:
            pass

    return images


def llm_reply(message, history=None):
    history = [
        {"role": item["role"], "content": item["content"]}
        for item in (history or [])
        if isinstance(item, dict)
        and item.get("role") in ["user", "assistant"]
        and isinstance(item.get("content"), str)
    ]
    mentioned_destinations = destinations_in_text(message)
    budget_context = budget_for_message(message, history)
    review_words = ["review", "reviews", "rating", "ratings", "complaint", "complaints", "negative", "positive", "bad", "good"]
    asks_about_reviews = any(word in message.lower() for word in review_words)
    trip_words = ["trip", "travel", "visit", "vacation", "holiday", "getaway", "honeymoon", "itinerary", "recommend", "suggest", "destination", "where should", "plan"]
    has_trip_context = bool(budget_context) or (bool(mentioned_destinations) and asks_about_reviews) or any(word in message.lower() for word in trip_words) or any(
        item["role"] == "user" and any(word in item["content"].lower() for word in trip_words)
        for item in history
    )
    if not has_trip_context:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are Traivo, a travel-planning chatbot. Briefly introduce yourself only if asked. Use the conversation history to understand follow-up questions. Answer only what the user specifically asked, in a concise response. If they ask about one aspect, answer only that aspect. Do not add destination recommendations unless requested. If a budget estimate is supplied, do not calculate another amount; the exact model estimate will be included after your answer."},
                *history,
                {"role": "user", "content": message + ("\n\nBudget estimate from the trained model: " + budget_context if budget_context else "")}
            ],
            temperature=0.2,
            max_completion_tokens=500,
            reasoning_effort="low"
        )
        reply = (response.choices[0].message.content or "").strip() or "I'm Traivo, your travel-planning assistant. What would you like help with?"
        attraction_context = attractions_for_message(message, history)
        return reply + ("\n\n" + budget_context if budget_context else "") + attraction_context

    preferences = user_input_organizer(message, history)
    response_content = model_response(preferences, mentioned_destinations or None)
    context = "\n".join(
        f"{destination}: travelers liked {reviews['positive']} Things to consider: {reviews['negative']}"
        for destination, reviews in response_content.items()
    )
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are Traivo, a travel-planning chatbot. Use the conversation history to understand follow-up questions. Answer only what the user asks, concisely, using the provided destination and review information. If the user asks for negative reviews, use only the negative review information; if they ask for positive reviews, use only the positive review information. Do not claim that a destination has no reviews unless the provided information says so. For recommendations, put the best match first and include other options only if useful. Do not dump every review detail. If a budget estimate is supplied, do not calculate another amount; the exact model estimate will be included after your answer."},
            *history,
            {"role": "user", "content": f"Request: {message}\n\nDestination and review information:\n{context}" + ("\n\nBudget estimate from the trained model: " + budget_context if budget_context else "")}
        ],
        temperature=0.2,
        max_completion_tokens=600,
        reasoning_effort="low"
    )
    reply = (response.choices[0].message.content or "").strip() or "I couldn't create a travel suggestion just now. Please try your request again."
    attraction_context = attractions_for_message(message, history)
    return reply + ("\n\n" + budget_context if budget_context else "") + attraction_context



#print(llm_reply("I like beach vibes suggest me a place to trip"))

    

