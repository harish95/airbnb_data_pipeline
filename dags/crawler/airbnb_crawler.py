import os
from os.path import exists

import requests
import re
from datetime import datetime
import gzip
import pandas as pd
from io import BytesIO



def get_dates(url):
    response = requests.get(url)
    html_content = response.content.decode('utf-8')

    # Extract dates in the format "dd MonthName, yyyy" using regex
    date_pattern = r"\b\d{1,2} \b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b, \d{4}"
    dates = re.findall(date_pattern, html_content)

    # Convert extracted dates to datetime objects and get the latest one
    date_objs = [datetime.strptime(date, "%d %B, %Y") for date in dates]

    latest_date = max(date_objs).date()
    return latest_date


def get_listing_data(date, city, state, country):
    # Create the URL based on the parameters
    url = f"https://data.insideairbnb.com/{country}/{state}/{city}/{date}/data/listings.csv.gz"
    print(url)
    # Download the data
    response = requests.get(url)
    if response.status_code == 200:
        print(response.status_code)
        # Decompress the .gz content
        with gzip.open(BytesIO(response.content)) as gz_file:
            # Load into a DataFrame
            df = pd.read_csv(gz_file)

        # Define the local path to save the CSV
        file_path = f"/opt/airflow/data/input/{city}_{date}_listings.csv"

        # Save DataFrame as .csv
        df.to_csv(file_path, index=False)

        print(f"Data saved to {file_path}")

        return "clean_data"
    else:
        print(f"Failed to download data. Status code: {response.status_code}")
        return "data_not_updated"

