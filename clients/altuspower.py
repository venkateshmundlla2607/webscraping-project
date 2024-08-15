import time
from bs4 import BeautifulSoup
from base import Scrapping
import re


class AltusPower(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/about-us/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        p_tags = soup.find_all('p')
        # Extract the text from the first two <p> tags and combine them into one string
        about_us = ' '.join(p.get_text() for p in p_tags[:2])
        return about_us

    def get_contacts(self):
        url = f"{self.url}/about-us/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        company_address = []
        div_tag = soup.find('div', class_='footer-contact-details')
        address_lines = [line.strip() for line in div_tag.find('p').contents if isinstance(line, str) and not line.startswith('Phone') and not line.startswith('Fax')]
        # Extract the phone number and fax number
        phone = div_tag.find('a', href=True).get_text()
        fax = div_tag.find_all('a', href=True)[1].get_text()
        # Combine the address lines into a single string
        address = ' '.join(address_lines)
        company_address.append(address)
        return company_address

    def get_news(self):
        url = f"{self.url}/blog/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        latest_news = []
        # Find all elements that might contain the blog information
        items = soup.find_all(['div', 'a'], class_=['blog-header_item w-dyn-item', 'blog-header_title-link w-inline-block'])
        # Iterate over the found items and extract details
        for item in items:
            try:
                # Extract URL
                url_element = item.find('a', class_='blog-header_image-link')
                url = url_element['href'] if url_element else 'No URL found'
                # Extract title
                title_element = item.find('a', class_='blog-header_title-link')
                if title_element:
                    title = title_element.find('h3').get_text(strip=True) if title_element.find('h3') else 'No title found'
                else:
                    title_element = item.find('div', class_='blog-header_title-link')
                    title = title_element.get_text(strip=True) if title_element else 'No title found'
                # Extract date
                date_element = item.find('div', class_='blog4-header_date-wrapper')
                date = date_element.find('div', class_='text-size-small').get_text(strip=True) if date_element and date_element.find('div', class_='text-size-small') else 'No date found'
                # Extract summary
                summary_element = item.find('p', class_='text-size-regular text-style-3lines')
                summary = summary_element.get_text(strip=True) if summary_element else 'No summary found'
                # Only add to the list if a valid title is found
                if title != 'No title found':
                    latest_news.append({
                    'title': title,
                    'date': date,
                    'url': self.url + url,
                    'summary': summary})
            except Exception as e:
                print(f"An error occurred: {e}")
        return latest_news

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        img_tags = soup.find_all('img', class_='customer_logo')
        company_names = []
        for img in img_tags:
            src = img['src'].split('/')[-1]  # Get the last part of the src attribute
            name_parts = re.split(r'_|%26|%20|\.svg', src)  # Split by underscores, URL encoding, and the file extension
            name = ' '.join([part for part in name_parts if not re.search(r'\d|logo|Logo|wordmark', part)]).strip()  # Remove unwanted parts
            if name not in company_names:
                company_names.append(name)
        return company_names
