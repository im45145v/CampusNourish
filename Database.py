import time
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import streamlit as st


client = MongoClient('mongodb+srv://[username]:[pass]@cluster0.ub5pbd6.mongodb.net/',serverSelectionTimeoutMS=60000)
db = client["Food"]
collection = db["Recipes"]

def check_for_ingredients():
    with open("ingredients.txt", "r") as file:
        ingredients_input = file.read()

    if ingredients_input:
    # Split the text by comma
        ingredients = ingredients_input.split()

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            results = collection.find()
            for document in results:
                for ingredient in ingredients:
                    if ingredient in document['ingredients']:
                        st.write(document)

            client.close()
            break  # Connection successful, exit the loop
        except ServerSelectionTimeoutError:
            print(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print(f"Unable to establish a connection after {max_retries} attempts. Exiting.")
