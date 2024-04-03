# ISD110 Staff Directory Scraper

This Scrapy spider (`isd110`) is designed to scrape staff directory information from the ISD110 (Independent School District 110) website. It extracts details such as school name, address, state, ZIP code, staff names, titles, phone numbers, and emails.

## Setup

1. Clone the repository: git clone <repository_url>
2. Install Scrapy (assuming Python is already installed): pip install scrapy

## Usage

1. Navigate to the project directory: cd <project_directory>
2. Run the spider using the following command: scrapy runspider .\isd110.py

## Spider Details

- **Spider Name:** isd110
- **Output Format:** CSV
- **Output File:** staff directory.csv

## Dependencies

- Python 3.x
- Scrapy

## Additional Notes

- The spider extracts staff directory information from the ISD110 website.
- The output is saved in CSV format as specified in the custom settings.
- Ensure that you have Scrapy installed before running the spider.
- The spider will create a CSV file named "Staff Directory.csv" to save the scraped data.
