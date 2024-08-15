import time
from bs4 import BeautifulSoup
from base import Scrapping
import re


class Prewave(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        carousel_wrapper = soup.find('div', class_='elementor-image-carousel-wrapper')
        container = soup.find_all('div', class_='e-con-inner')[6]
        # Initialize result
        about_company = []
        # Check if the container is found
        if container:
            h2_tag = container.find('h2')
            p_tag = container.find('p')
            if h2_tag and p_tag:
                combined_text = h2_tag.get_text(strip=True) + " " + p_tag.get_text(" ", strip=True)
                about_company.append(combined_text)
        data = " ".join(about_company)
        return data

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        carousel_wrapper = soup.find('div', class_='elementor-image-carousel-wrapper')
        # Extract the alt tag data and clean up the company names
        company_names = []
        if carousel_wrapper:
            img_tags = carousel_wrapper.find_all('img')
            for img in img_tags:
                alt_text = img.get('alt', '')
                company_name = (alt_text.split('_')[0]).split('-')[0]  # Split by underscore and take the first part
                company_names.append(company_name)
        return company_names

    def get_news(self):
        url = f"{self.url}/news/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        latest_news = []
        div_tag = soup.find_all('div', class_='elementor-widget-container')[24]
        h2_tag = div_tag.find('h2', class_= 'elementor-heading-title elementor-size-default')
        title = h2_tag.get_text(strip=True) if h2_tag else 'Title not found'
        a_tag = div_tag.find('a',class_="elementor-button elementor-button-link elementor-size-sm")
        url = a_tag['href'] if a_tag else 'URL not found'
        latest_news.append({'title': title,
            'url':url})
        #print(latest_news)
        url = latest_news[0]['url']
        self.driver.get(url)
        page_source = self.driver.page_source
        soup1 = BeautifulSoup(page_source, 'html.parser')

        div_tag = soup1.find('div', class_='elementor-element elementor-element-9d0307b ob-has-background-overlay elementor-widget elementor-widget-theme-post-content')
        #print(div_tag)
        if div_tag:
            # Find the <p> tags within this <div>
            p_tags = div_tag.find_all('p')

            # Function to clean the text
            def clean_text(text):
                return re.sub(r'^\s*●\s*', '', text).strip()

            # Extract and clean text from the first two <p> tags and concatenate
            if len(p_tags) >= 2:
                summary = ' '.join(clean_text(p.get_text()) for p in p_tags[1:3])
            else:
                summary = 'Not enough <p> tags found.'
            latest_news[0]['summary'] = summary
        
        span_tag = soup.find('span', class_='elementor-post-info__item-prefix')
        if span_tag:
            # Find the text node immediately following the span tag
            next_sibling = span_tag.find_next_sibling()
    
            if next_sibling and next_sibling.string:
                # Extract and strip the text
                date_text = next_sibling.string.strip()
                latest_news[0]['date'] = date_text

 
        return latest_news
