## Overview:

This project involves scraping data from websites for analysis and processing. 

## Features
- ScrapesScrapes data from multiple websites
- Handles different types of data formats
- Extracts key-value pairs or other structured data
- Saves data in CSV or JSON formats

## Requirements
- Python 3.x
- Libraries:
- requests for HTTP requests
- BeautifulSoup for parsing HTML
- selenium


## how to run

## Navigate to the Project Files Folder:

- Open your file explorer or terminal and go to the folder containing your project files.
- Retrieve the ID from constants.py:
- Open the constants.py file and find the relevant ID value you need.
- Open a Terminal:
- In the project folder, open a terminal or command prompt.
- Run the main.py Script:
- To run the script with a specific ID:
- python main.py -c <id>
- Replace <id> with the actual ID you retrieved from constants.py. For example: python main.py -c 65212
- to scrape mutiple <id>'s them give the id's as in comma(,) seprated values. For example: python main.py -c 12605,2805,65212 
- To scrape all available data without specifying an ID: python main.py

# Specify Output Format (Optional):
- By default, the output will be saved as a CSV file. If you want to change the format to JSON, use:
- python main.py -c <id> -o json
- Again, replace <id> with the actual ID if needed. For example: python main.py -c 65212 -o json
# Locate the Output File:

The output file will be saved in the project folder. Name of the file: output<timestamp>.csv/output<timestamp>.json

# Note:

Update the selenium driver in the utlis.py as per the operating system.

remove comment in the line no. 16 and add comment no. 14 if operating system is windows.

remove comment in the line no. 14 and add comment no. 16 if operating system is MacOS.
