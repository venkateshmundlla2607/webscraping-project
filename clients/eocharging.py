import time
from bs4 import BeautifulSoup
from base import Scrapping
import re


class EoCharging(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/our-mission/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div = soup.find('div', class_='text-left sm:w-[40%] order-first sm:order-second sm:ml-auto')
        about_company = []
        # Extract the text from h5 and p tags
        if div:
            h5_text = div.find('h5').get_text(strip=True) if div.find('h5') else ''
            p_texts = [p.get_text(strip=True) for p in div.find_all('p')]
            # Combine h5 and p texts into one string
            about_us = ' '.join([h5_text] + p_texts)
            about_company.append(about_us)
        data = " ".join(about_company)
        return data

    def get_news(self):
        url = f"{self.url}/stories/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        articles = soup.find_all('a', class_='group relative text-left border-1 border-gray-300 rounded-2.5xl flex flex-col justify-between bg-gray-300 h-full')
        news = []
        for article in articles:
            title = article.find('h5').get_text(strip=True)
            #print(title)
            description = article.find('p').get_text(strip=True)
            #image_url = article.find('img')['src']
            link = article['href']
            news.append({
                'title':title,
                'url': self.url + link
                    })
        #print(news[0]['url'])
        url = news[0]['url']
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup1 = BeautifulSoup(page_source, 'html.parser')
        latest_news = []
        latest_news.append(news[0])
        date = soup1.find('span', class_='mt-4 md:mt-0').text.strip()
        #print(date)
        # Extract the first 1 to 4 <p> tags with non-empty content
        p_tags = soup1.find_all('div', id='rich-text-wrapper')[0].find_all('p')
        summary = ' '.join(p.get_text(strip=True) for p in p_tags[:3] if p.get_text(strip=True))
        #print(summary)
        latest_news[0]['date'] = date
        latest_news[0]['summary'] = summary
        return latest_news

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        pictures = soup.find_all('picture', class_='px-4')
        # Extract and clean company names
        company_names = []
        for picture in pictures:
            img_tag = picture.find('img')
            if img_tag and 'alt' in img_tag.attrs:
                company_name = img_tag['alt']
                # Remove the word "Logo" or "logo"
                cleaned_name = company_name.replace(" Logo", "").replace(" logo", "")
                if cleaned_name not in company_names:
                    company_names.append(cleaned_name)
        return company_names
