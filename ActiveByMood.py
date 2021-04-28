#########################################
##### Name: Soo Ji Choi             #####
##### Uniqname: soojc               #####
#########################################

"""
Documentations and Tutorials:
- https://www.youtube.com/watch?v=th5_9woFJmk&ab_channel=CoreySchafer
- https://github.com/googleapis/google-api-python-client

____________________
STEPS to API:
1. Retrieve Youtube Data v3 API key
2. Downloaded google-api-python-client
    in terminal - pip install google-api-python-client
3. Set up to call API on python
    service name = 'youtube'
    service version = 'v3'
    youtube = build('youtube', 'v3', developerKey=api_key)
4. Test request
    Methods available for use: https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
____________________
-*- coding: utf-8 -*-
Sample Python code for youtube.search.list

See instructions for running these code samples locally:
https://developers.google.com/explorer-help/guides/code_samples#python

"""

import requests
import json
import os

import sqlite3

import plotly.graph_objects as graph

import googleapiclient.discovery
from googleapiclient.discovery import build
import googleapiclient.errors

import secrets

CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

def load_cache():
    '''Open cache file and load JSON into CACHE_DICT.
    If cache file doesn't exist, create a new cache dict.

    Parameters
    -------------------
    None

    Returns
    -------------------
    cache dict
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache_dict = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    '''Saves the current state of the cache

    Parameters
    -------------------
    cache_dict: dict

    Returns
    -------------------
    none
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache_dict)
    cache_file.write(contents_to_write)
    cache_file.close()

class MoodAssistant():
    """Representation of user state (mood) and sugggested video category

    Attributes:
        Instance variables are generated when an instance is instantiated based on
        the passed in function

    Methods:
        info: print out instance values in a string format
    """
    def __init__(self, mood="None", title="None", channel="None", video_id="None", json=None):
        """Initialize MoodAssistant instance. Loops over the passed in dictionary and
            generate each instance variable and assign the value.

        Parameters:
            mood (string): string representation of mood state of "positive", "neutral", or "negative"
            title (string): string representation of Youtube video title
            channel (string): string representation of content creator's channel
            video_id (string): string representation of Youtube video ID
            json (dict): dictionary containing each search result

        Returns:
            None
        """

        if (json is None):
            self.mood = mood
            self.title = title
            self.channel = channel
            self.video_id = video_id
            self.json = json
        else:
            self.title = json['snippet']['title']
            self.channel = json['snippet']['channelTitle']
            self.video_id = json['id']['videoId']

    def info(self):
        """Returns a string representation of title, author and release year objects
        per the following format:
        <title> by <creator> (<url>)
        """
        return f"{self.title} by {self.channel} \n(Click to start: http://www.youtube.com/embed/{self.video_id}) \f"

def categorize_mood(input_mood):
    """Accepts user's response to mood evaluation, and categorizes the response into mood state.
    Parameters:
        input_mood(int): User's rating of mood from 1-5

    Returns:
        string: mood_state of either "positive", "neutral" or "negative"
    """
    if 1 <= input_mood <= 2:
        mood_state = "negative"
    elif input_mood == 3:
        mood_state = "neutral"
    elif 4 <= input_mood < 6:
        mood_state = "positive"
    else:
        pass

    return mood_state

def retrieve_search(mood_state):
    """Accepts an input query, requests an API search, and returns a JSON-friendly
    list of dictionaries.

    Parameters:
        mood_state (str): User's mood state based on input

    Returns:
        list of dictionaries: list of dictionary representations of the decoded JSON document
    """
    api_service_name = "youtube"
    api_version = "v3"
    api_key = secrets.API_KEY

    youtube = build(api_service_name, api_version, developerKey=api_key)

    if mood_state == "negative":
        request = youtube.search().list(
            part="snippet",
            maxResults=3,
            order="rating",
            q="home yoga exercise for stress relief",
            type="video",
            videoDuration="medium"
        )

    elif mood_state == "neutral":
        request = youtube.search().list(
            part="snippet",
            maxResults=3,
            order="rating",
            q="low impact home workout",
            type="video",
            videoDuration="medium"
        )

    elif mood_state == "positive":
        request = youtube.search().list(
            part="snippet",
            maxResults=3,
            order="rating",
            q="home hiit workout",
            type="video",
            videoDuration="medium"
        )


    if mood_state in CACHE_DICT.keys():
        retrieved_json = CACHE_DICT[mood_state]
        print("Using Cache...")
    else:
        CACHE_DICT[mood_state] = request.execute()
        retrieved_json = CACHE_DICT[mood_state]#.json()
        #print(retrieved_json)
        save_cache(CACHE_DICT)
        print("Fetching...")

    return retrieved_json

def create_instance(mood_state, json): #json takes in retrieved_json, which has a list of dictionaries
    """Accepts a list of dictionaries retrieved from API search,
    sorts each dictionary into categories & create instance.

    Parameters:
        json (list): list of dictionaries

    Returns:
        string: information about the instances
    """
    mood_instance = MoodAssistant(mood=mood_state, json=json)

    return mood_instance.info()

def save_to_database(mood_value, mood_state):
    """Accepts a string representation of mood state, and save the state to sql database

    Parameters:
        mood_state (str): string representation of a mood state
        "positive", "neutral" or "negative"

    Returns:
        string: information about the instances
    """
    conn = sqlite3.connect("MoodLog.sqlite", timeout=10)
    cur = conn.cursor()

    # drop_table = '''
    #     DROP TABLE IF EXISTS "UserMood";
    # '''

    #conn.create_function("current_mood", 1, mood_state)

    create_table = '''
        CREATE TABLE IF NOT EXISTS "UserMood" (
            "ID"	INTEGER UNIQUE,
            "Mood_value"    TEXT NOT NULL,
            "Mood_state"	TEXT NOT NULL,
            "Date" DATE NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
    '''

    insert_data = '''
        INSERT INTO UserMood VALUES (
            NULL,
            ?,
            ?,
            datetime('now')
    )
    '''

    #cur.execute(drop_table)
    cur.execute(create_table)
    cur.execute(insert_data, (mood_value, mood_state,))

    conn.commit()

def query_recent_12():
    mood_value = []
    mood_state = []
    date = []

    conn = sqlite3.connect("Moodlog.sqlite", timeout=10)
    cur = conn.cursor()

    query = '''
        SELECT * FROM (
        SELECT * FROM UserMood ORDER BY ID DESC LIMIT 12)
        ORDER BY ID ASC;
    '''
    cur.execute(query)

    results = cur.fetchall()
    #results == [(1, '5', 'positive', '2021-04-28 20:22:08'), (2, '5', 'positive', '2021-04-28 20:22:33')]

    for each_result in results:
        mood_value.append(each_result[1])
        mood_state.append(each_result[2])
        date.append(each_result[3])

    return mood_value, mood_state, date

def call_mood_graph(mood_value, mood_state, date):
    """Retrieve 30 mood data from sql databse, and visualize the data using plotly

    Parameters:
        mood_value (from SQL Database)
        mood_state (from SQL Database)
        date (from SQL Database)

    Returns:
        None (auto open HTML)
    """
    # dates = ["4-28", "4-29", "4-30", "5-1", "5-2"]
    # mood_value = [4, 2, 5, 4, 3]
    # mood_state = ["positive", "negative", "positive", "positive", "neutral"]

    scatter_data = graph.Scatter(
        x=date,
        y=mood_value,
        text=mood_state,
        marker={'symbol':'circle', 'size':12, 'color': 'royalblue'},
        mode='lines+markers+text',
        textposition="top center",
        line=dict(color='royalblue', width=4))

    basic_layout = graph.Layout(
        title='Overview of Your Recent Mood',
        xaxis_title='Date',
        yaxis_title='Mood')

    fig = graph.Figure(
        data=scatter_data,
        layout=basic_layout
    )

    fig.update_yaxes(categoryorder="category ascending")

    fig.write_html("Mood_Overview.html", auto_open=True)

def main():
    exercise_list = []

    print("---------------------------")
    print("Launching [ActiveByMood]!")
    print("...")
    INPUT_QUERY = input('How do you feel today? Please rate your response between 1-5 from Very bad, Bad, Okay, Good, Very good: ').lower()
    counter = 0
    #valid_state = ["positive", "neutral", "negative"]

    while True:
        if isinstance(INPUT_QUERY, str): #if string
            if INPUT_QUERY.isnumeric(): #numeric string
                INPUT_QUERY = int(INPUT_QUERY)
            elif INPUT_QUERY == "exit": #exit
                print("Bye!")
                print("----- END OF PROGRAM -----")
                break
            elif INPUT_QUERY == "review mood":
                mood_value, mood_state, date = query_recent_12()
                call_mood_graph(mood_value, mood_state, date)
                #call_mood_graph() #show the last 10 moods in a graph
                INPUT_QUERY = input('Start exercise by clicking the URL or "exit": ')

            else: #other word string
                print("1 ERROR: Invalid numeric value. Enter a number between 1 to 5.")
                INPUT_QUERY = input('How do you feel today? Please rate your response between 1-5 from Very bad, Bad, Okay, Good, Very good: ').lower()

        if isinstance(INPUT_QUERY, int): #if converted to int
            if 1 <= INPUT_QUERY < 6: #if a valid mood state
                user_mood_state = categorize_mood(INPUT_QUERY)
                suggested_exercise_dict = retrieve_search(user_mood_state)

                for each_dict in suggested_exercise_dict['items']:
                    exercise_list.append(create_instance(user_mood_state, each_dict))

                save_to_database(INPUT_QUERY, user_mood_state)
                print("Thank you. Your mood has been logged.")

                print("Based on your mood today, Here are your suggested exercise videos:")
                print("---------------------------")
                for each_info in exercise_list:
                    counter += 1
                    print(f"{counter}. {each_info}")

                # reset response
                counter = 0
                exercise_list = []

                print("---------------------------")
                INPUT_QUERY = input('Start exercise by clicking the URL, "review mood" to view your past mood trajectory, or "exit": ').lower()

            else:
                print("2 ERROR: Invalid numeric value. Enter a number between 1 to 5.")
                INPUT_QUERY = input('How do you feel today? Please rate your response between 1-5 from Very bad, Bad, Okay, Good, Very good: ').lower()


if __name__ == "__main__":
    CACHE_DICT = load_cache()
    main()
