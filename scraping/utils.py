import csv
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_webdriver():
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless mode, without opening a browser window

    # Mac: Replace with the actual path to your chromedriver
    service = Service(executable_path='/opt/homebrew/Caskroom/chromedriver/127.0.6533.99/chromedriver-mac-arm64/chromedriver')

    # Windows: Replace with the actual path to your chromedriver
    #service = Service(executable_path=r'chromedriver-win64\chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def print_data(c_objs, output_type="csv"):
    if output_type == "csv":
        write_csv(c_objs)
    elif output_type == "json":
        write_json(c_objs)


def write_csv(c_objs):
    data = []
    for obj in c_objs:
        obj.data['id'] = obj.cid
        obj.data['name'] = obj.name
        obj.data['url'] = obj.url
        data.append(obj.data)

    headers_order = []
    news_headers = []

    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    file_name = f"output_{timestamp}.csv"

    # Determine the order of headers and valid headers with actual data
    for item in data:
        for key in item:
            if key == 'news':
                if item[key]:  # Only include 'news' fields if there's data
                    for i, news_item in enumerate(item[key]):
                        for k in news_item:
                            header_key = f"news_{k}_{i + 1}"
                            if header_key not in news_headers:
                                news_headers.append(header_key)
            else:
                if key not in headers_order:
                    headers_order.append(key)

    # Combine main headers with news headers
    headers_order.extend(news_headers)

    # Write the CSV file with the correct column order and only non-empty columns
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers_order)
        writer.writeheader()

        for item in data:
            row = {key: '' for key in headers_order}

            # Fill row with data
            for key in item:
                if key == 'news':
                    if item[key]:  # Only add news fields if there is data
                        for i, news_item in enumerate(item[key]):
                            for k in news_item:
                                header_key = f"news_{k}_{i + 1}"
                                if header_key in row:
                                    row[header_key] = news_item[k]
                elif isinstance(item[key], list):
                    if item[key]:  # Only add if the list is not empty
                        row[key] = '; '.join(map(str, item[key]))
                else:
                    if item[key]:  # Only add if there is data
                        row[key] = item[key]

            # Only write the row if it has at least one non-empty column
            if any(row[key] for key in row):
                writer.writerow(row)

    print(f"CSV file {file_name} created successfully.")


def write_json(c_objs):
    obj_data = []
    for obj in c_objs:
        obj.data['id'] = obj.cid
        obj.data['name'] = obj.name
        obj.data['url'] = obj.url
        obj_data.append(obj.data)

    new_data = json.dumps(obj_data, indent=4)

    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    file_name = f"output_{timestamp}.json"
    with open(file_name, "w") as file:
        file.write(new_data)

    print(f"JSON file {file_name} created successfully.")
