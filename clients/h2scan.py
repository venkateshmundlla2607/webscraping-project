import time
from bs4 import BeautifulSoup
from base import Scrapping
import re


class H2Scan(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        about_us = []
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        about_company = soup.find('div', class_='elementor-heading-title').text.strip()
        about_us.append(about_company)
        data = " ".join(about_us)
        return data

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div', class_='elementor-widget-wrap elementor-element-populated e-swiper-container')
        # Extract company names from the 'alt' attribute of <img> tags
        company_names = []
        if target_div:
            img_tags = target_div.find_all('img')
            company_names = [img['alt'].capitalize() for img in img_tags if 'alt' in img.attrs]
        return company_names

    def get_news(self):
        url = f"{self.url}/resource-gallery/?filter=.press-release/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        news = []
        # Loop through each title and corresponding date and link
        for title_div in soup.find_all('div', class_='row title pt-2 px-2'):
            title = title_div.find('h3').text.strip()
            date_div = title_div.find_next('div', class_='row summary pb-2 px-2')
            date = date_div.find('p').text.strip()
            link_div = title_div.find_next('div', class_='row link pt-5 pb-5 px-2')
            url = link_div.find('a')['href']

            news.append({
                'title': title,
                'date': date,
                'url': url
            })
        latest_news = []
        latest_news.append(news[0])
        url = news[0]['url']
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        page_source = self.driver.page_source
        soup1 = BeautifulSoup(page_source, 'html.parser')
        target_div = soup1.find('div',
                                class_='elementor-element elementor-element-5494fbe post-text elementor-widget elementor-widget-theme-post-content')
        # Extract and print the text from the first <p> tag within the target <div>
        if target_div:
            first_p_tag = target_div.find('p')
            if first_p_tag:
                summary = first_p_tag.get_text()
                latest_news[0]['summary'] = summary
        return latest_news

    def get_contacts(self):
        url = f"{self.url}/service/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div',
                               class_='elementor-element elementor-element-4cc7d16 elementor-widget elementor-widget-text-editor')
        company_address = []
        if target_div:
            first_p_tag = target_div.find('p')
            if first_p_tag:
                # Replace <br/> tags with a space
                for br_tag in first_p_tag.find_all('br'):
                    br_tag.insert_after(' ')
                    br_tag.decompose()
                # Get the text and format it
                text = first_p_tag.get_text(separator=' ', strip=True)
                # Ensure only one space between lines
                address = ' '.join(text.split())
                company_address.append(address)
                # print(address)
            else:
                print("No <p> tag found in the specified <div>.")
        else:
            print("No <div> with the specified class found.")
        return company_address
