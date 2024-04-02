# NevadaEPro Scrapy Spider

This Scrapy spider is designed to scrape data from the NevadaEPro website (https://nevadaepro.com/). It extracts information about bids and downloads associated files.

## Installation

1. Clone the repository: git clone <repository_url>
2. Install Scrapy (assuming Python is already installed): pip install scrapy

## Usage

1. Navigate to the project directory.
2. Run the spider using the following command: scrapy runspider .\nevadaepro.py
3. The spider will start scraping the website and saving the data in JSON format.

## Spider Details

- **Spider Name:** nevadaepro
- **Output Format:** JSON
- **Output File:** nevadaepro.json

## Dependencies

- Python 3.x
- Scrapy

## Additional Notes

- The spider will create a directory named "Attachments Files" to save downloaded files associated with the bids.
- Ensure that you have proper permissions to write to the disk for saving files.


