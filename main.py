import requests
import pandas as pd
import logging
import time
import pickle
from sklearn.preprocessing import StandardScaler
import json


def retrieve_data():
    """
    Makes an API request to retrieve cyber threat data and saves it to a file.
    """
    # Set the URL for the data source
    url = "https://google.com"

    # Set the API key for the data source
    api_key = "92fc4c35-c5c0-4a9e-bebc-8329e6517bda"

    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Set the parameters for the API request
    params = {
        "start_date": "2023-01-04",
        "end_date": "2020-01-08",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        print("Error: Could not make request due to network error.")
        return

    # Check the status code of the response
    if response.status_code == 200:
        # If the request is successful, parse the JSON response and save it to a file
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            print("Error: Could not parse response as JSON. Here is the raw response:")
            print(response.text)
            return
        with open("cyber_threat_data.json", "w") as f:

            json.dump(data, f)
            print("File created and written to successfully.")
            # Print the contents of the file to check that it has been written correctly
            print(f"File contents: {data}")
    else:
        # If the request is unsuccessful, print an error message
        print(f"Error: Could not retrieve data. Status code: {response.status_code}")





def train_model():
    # Load the data from the file
    with open("cyber_threat_data.json", "r") as f:
        # Print the contents of the file to check that it is a properly formatted JSON object
        data = f.read()
        if data:
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError as e:
                print("Error: Could not parse data as JSON. Here is the raw data:")
                print(data)
                return
        else:
            print("Error: Data file is empty.")
            return


def collect_data():
    """
    Collects data on network activity.
    """
    # Replace this with code to collect data on network activity
    return [
        {"f1": 1, "f2": 2, "f3": 3},
        {"f1": 4, "f2": 5, "f3": 6},
        {"f1": 7, "f2": 8, "f3": 9},
    ]

def preprocess_data(data):
    """
    Preprocesses collected data on network activity.
    """
    # Convert the data into a pandas DataFrame
    data = pd.DataFrame(data)

    # Normalize the data
    scaler = StandardScaler()
    X = scaler.fit_transform(data[["f1", "f2", "f3"]])

    return X


def detect_threats():
    """
    Continuously collects data on network activity and flags potential threats.
    """
    # Load the trained machine learning model
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Error: Could not find file 'model.pkl'. Please make sure the file exists and is in the correct directory.")
        return

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Continuously collect data on network activity
    while True:
        data = collect_data()
        X = preprocess_data(data)
        y_pred = model.predict(X)
        if y_pred.any():
            logging.warning("Possible cyber threat detected!")
        time.sleep(60)


def main():
    retrieve_data()
    train_model()
    detect_threats()

if __name__ == "__main__":
    main()
