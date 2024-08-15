import time
from bs4 import BeautifulSoup
from base import Scrapping


class InfinitedFiberCompany(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/about-us/"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        about_us = []
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            about_us.append(paragraph.get_text(strip=True))
        if about_us:
            return about_us[0]
        else:
            return ""

    def get_contacts(self):
        url = f"{self.url}/contact/"
        self.driver.get(url)

        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        map_blocks = soup.find_all('div', class_='wp-block-into-digital-map')

        # Extract the information
        locations = []
        for block in map_blocks:
            title = block.find('h2', class_='wp-block-heading title').get_text(strip=True)
            address = block.find('p', class_='description').get_text(strip=True)
            locations.append(address)
        return locations

    def get_news(self):
        url = f"{self.url}/news/"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        latest_article = soup.find('article')
        url1 = latest_article.find('a')['href']
        title = latest_article.find('h3', class_='post-title').get_text(strip=True)
        date = latest_article.find('div', class_='date').get_text(strip=True)

        self.driver.get(url1)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source1 = self.driver.page_source
        soup1 = BeautifulSoup(page_source1, 'html.parser')
        heading = soup1.find('strong').get_text(strip=True)
        paragraphs = soup1.find_all('p')
        # content = paragraphs[0].get_text(strip=True)

        latest_info = {
            'title': title,
            'date': date,
            'url': url1,
            'content': heading
        }
        return [latest_info, ]
