# Airbnb Data Pipeline
This project is a data engineering pipeline designed to automate the collection, processing, and storage of Airbnb data. The pipeline downloads a CSV file from a specified URL, subsets it to retain only the relevant columns, and stores the processed data in an S3 bucket. The entire flow is automated using Apache Airflow, which runs in a Docker container.

## Project Overview
The purpose of this project is to streamline the process of acquiring, filtering, and storing Airbnb data in a scalable and automated way. By using Apache Airflow within Docker, the pipeline can be scheduled to run at regular intervals, ensuring up-to-date data availability.

## Features
1. **Data Download**: Downloads a CSV file from a given URL using the requests library.
2. **Data Processing**: Selects a subset of 57 columns from the original dataset.
3. **Storage**: Stores the processed data in an S3 bucket.
4. **Automation**: Automated data flow using Apache Airflow in a Docker container.

## Technologies Used
1. **Python**: For data download and processing.
2. **Apache Airflow**: To automate and orchestrate the data pipeline.
3. **Docker**: To containerize the Airflow environment.
4. **AWS S3**: For cloud storage of processed data.

