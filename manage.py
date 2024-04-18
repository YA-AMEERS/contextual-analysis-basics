from flask import Flask, render_template, url_for, session, request, jsonify, redirect
from app import models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import timedelta
import hashlib as h
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from dateutil.parser import parse
import random
import string
from app import create_app, db
from app.models.models import UptodateNews, AllNews
import time
from dotenv import load_dotenv
import openai
import json


UPLOAD_FOLDER = "uploads"  # Create a folder named 'uploads' in your Flask app directory

load_dotenv()

app = create_app(os.getenv("BOILERPLATE_ENV") or "dev")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.app_context().push()
app.permanent_session_lifetime = timedelta(weeks=1)

migrate = Migrate(app, db)

openai.api_key = os.getenv("OPENAI-API-KEY")


def hashblock(req):
    encoded_block = json.dumps(req, sort_keys=True).encode()
    block_encryption = h.sha256()
    block_encryption.update((encoded_block))
    return block_encryption.hexdigest()


def random_number_between_0_and_9():
    """Generates a random integer between 0 and 9 (inclusive)."""
    return random.randrange(3)  # Stop at 3 (exclusive)


def delete_outDated_news():
    try:
        row_count = UptodateNews.query.count()
    except:
        db.session.rollback()
        row_count = UptodateNews.query.count()

    if row_count > 50:
        db.session.query(UptodateNews).delete()
        db.session.commit()
        print("Deleted all rows from UptodateNews table (count exceeded 10).")
        return True
    else:
        print("Row count within limits (current count: {}).".format(row_count))
        return False




def google_search(query):
    """Performs a basic Google search using requests and attempts to extract all text.

    Args:
        query (str): The search query to use.

    Returns:
        str: A large string containing all extracted text from the search results page
             (may be incomplete or inaccurate due to HTML structure and limitations).
    """

    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Your Name/Project"}  # Simulate a browser request
    response = requests.get(url, headers=headers)
    # print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text using a recursive function (may need further refinement)
        def extract_text(element):
            """Recursively extracts text from an HTML element and its children."""
            if element.text.strip():
                return element.text.strip() + "\n"
            else:
                return "".join(extract_text(child) for child in element.children)

        all_text = extract_text(soup)
        # print(all_text)
        return all_text
    else:
        print(f"Error: {response.status_code}")
        return None


def searchQuery(search_query):
    try:
        all_text = google_search(search_query)
    except:
        time.sleep(20)
        all_text = google_search(search_query)
    if all_text:
        # print(f"Extracted text:\n{all_text}")
        return all_text
    else:
        print("Error fetching search results.")
        return None


def generate(context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "you are a nigerian news analyst, only provide a RFC8259 compliant JSON response",
                "role": "user",
                "content": f"""you are given the following search result of news from google. your task is to extract breaking news with there headlines, and sort them in a json format like this:
                [{{
                "Headline":"head line of the first news in the text",
                "story": "the first story for the first headline in the text, rephrase it and emphasize, break it down while highlighting the key points. ",
                "source": "the source of the story and associated links"
                }},
                {{
                "Headline":"head line of the second news in the text",
                "story": "the second story for the second headline in the text, rephrase it and emphasize, break it down while highlighting the key points. ",
                "source": "the source of the story and associated links"
                }},
                ] and so on, do the same for all the storys in the text, make sure you attend through each and every story in the extracted text, for all the stories in the text, not just one story. make sure you return just the json format, don't add any text apart from the json.
                here is the text:  {context}""",
            },
        ],
        temperature=0.3,
        max_tokens=1473,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # return json.loads(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]



def searchSequentially(state, channel, section, country = "nigeria"):
    print(1)
    search_query = channel + " breaking news today in " + state + " on " + section
    text = searchQuery(search_query)
    try:
        extrctedFormatted = generate(text)
    except:
        time.sleep(40)
        extrctedFormatted = generate(text)
    # print(extrctedFormatted)
    try:
        jsonData = json.loads(extrctedFormatted)
    except:
        extrctedFormatted = generate(text)
        jsonData = json.loads(extrctedFormatted)
    
    for data in jsonData:
        
        number = random_number_between_0_and_9()

        news = UptodateNews(
            postId=hashblock(text),
            headLine=data["Headline"],
            story=data["story"],
            source=data["source"],
            grade=number,
            state=state,
            country=country,
            section=section,
            channel=channel
        )
        all_news = AllNews(
            postId=hashblock(text),
            headLine=data["Headline"],
            story=data["story"],
            source=data["source"],
            grade=number,
            state=state,
            country=country,
            section=section,
            channel=channel
        )
        try:
            
            db.session.add(news)
            db.session.add(all_news)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.add(news)
            db.session.commit()





def updateNews():
    # time.sleep(5000)
    print("updating news")

    delete_outDated_news()

    # start sequencial search and update
    searchSequentially("kano State", "BBC", "Business")
    searchSequentially("Abuja FCT", "BBC", "Business")
    searchSequentially("kaduna State", "BBC", "Business")
    searchSequentially("Bauchi State", "BBC", "Business")
    searchSequentially("kano State", "BBC", "Security")
    searchSequentially("Abuja FCT", "BBC", "Security")
    searchSequentially("kaduna State", "BBC", "Security")
    searchSequentially("Bauchi State", "BBC", "Security")
    searchSequentially("kano State", "BBC", "Health care")
    searchSequentially("Abuja FCT", "BBC", "Health care")
    searchSequentially("kaduna State", "BBC", "Health care")
    searchSequentially("Bauchi State", "BBC", "Health care")
    searchSequentially("kano State", "dailypost", "Security")
    searchSequentially("Abuja FCT", "dailypost", "Security")
    searchSequentially("kaduna State", "dailypost", "Security")
    searchSequentially("Bauchi State", "dailypost", "Security")
    searchSequentially("kano State", "dailypost", "Health care")
    searchSequentially("Abuja FCT", "dailypost", "Health care")
    searchSequentially("kaduna State", "dailypost", "Health care")
    searchSequentially("Bauchi State", "dailypost", "Health care")
    searchSequentially("kano State", "dailypost", "Business")
    searchSequentially("Abuja FCT", "dailypost", "Business")
    searchSequentially("kaduna State", "dailypost", "Business")
    searchSequentially("Bauchi State", "dailypost", "Business")
    searchSequentially("kano State", "channelstv", "Security")
    searchSequentially("Abuja FCT", "channelstv", "Security")
    searchSequentially("kaduna State", "channelstv", "Security")
    searchSequentially("Bauchi State", "channelstv", "Security")
    searchSequentially("kano State", "channelstv", "Health care")
    searchSequentially("Abuja FCT", "channelstv", "Health care")
    searchSequentially("kaduna State", "channelstv", "Health care")
    searchSequentially("Bauchi State", "channelstv", "Health care")
    searchSequentially("kano State", "channelstv", "Business")
    searchSequentially("Abuja FCT", "channelstv", "Business")
    searchSequentially("kaduna State", "channelstv", "Business")
    searchSequentially("Bauchi State", "channelstv", "Business")
   
    
    print("finished")
    return True


def is_date(string, fuzzy=True):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except:
        return False









    
updateNews()



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
