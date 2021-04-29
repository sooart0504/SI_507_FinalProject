# SI_507_FinalProject (Incomplete program | Data Checkpoint)
### Created by Soo Ji Choi

### Project Summary
A personalized health intervention program that suggests exercise videos based on the user's affective state, logs and displays the user’s overall affective state.

**Project Interaction Flow & Components**
* Program prompts for the user's current mood with a list of options
* User chooses their current mood
* Program saves the user input data into a database as an archive
  * All inputs are stored and saved to later view it as a data visualization
* Based on user input, the program identifies the user's affective state into a category that will be used to suggest a different types of exercise 
  * Positive emotion
    * Moderate to high intensity exercise
  * Neutral emotion
    *  Light intensity exercise
  * Negative emotion
    * Relaxation-focused exercise
* Then, the program suggests 3 youtube exercise video
  * If mood is negative, suggest relaxation exercise videos such as relaxation/breathing/meditation/yoga/stretching exercises
  * If mood is neutral, suggest light intensity exercise videos
  * If mood is positive, suggest moderate to high intensity exercise videos such as HIIT or cardio
* After the exercise video is suggested, user have several options:
  * User have the option to start exercise now (link to embedded youtube video)
  * View mood archive data
    * If requested to see archive data, program accesses the archive database of the recent 12 inputs, and plots the mood data into a plot (assuming the data was inputted by one user)
    * After displaying the data visualizations, the program has the option to start exercise or quit the program.
  * Quit the program

Data sources:
* Youtube Data API - used to search exercise videos
* SQLite Database with an archive of past user inputs
* Plotly - data visualization

**Required Packages**
1. import requests (for API)
2. import json (for API)
3. import os
4. import sqlite3 (for database)
5. import plotly.graph_objects (for data visualization)
6. import googleapiclient.discovery (for Youtube API)
7. import build from googleapiclient.discovery (for Youtube API)
8. import googleapiclient.errors (for Youtub API)
9. import secrets file (API key stored and imported from another file)
