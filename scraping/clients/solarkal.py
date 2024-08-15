import time
from bs4 import BeautifulSoup
from base import Scrapping
import re


class Solarkal(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/our-services/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_tag = soup.find('div', class_='_40-spacer')
        about_us = []
        if div_tag:
            p_tag = div_tag.find('p')
            if p_tag:
                about_company = p_tag.get_text(separator=' ').strip()
                about_us.append(about_company)
            else:
                print("No <p> tag found inside <div class='_40-spacer'>")
        data = " ".join(about_us)
        return data

    def get_contacts(self):
        url = f"{self.url}/contact-us/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        contact_wrap = soup.find('div', class_='contact-wrap dgreen-bg')
        company_address = []
        if contact_wrap:
            # Find the paragraph with class 'contact-p' which contains the address
            address_paragraph = contact_wrap.find('p', class_='contact-p')

            if address_paragraph:
                # Get the text of the address, replacing <br/> with spaces
                address = address_paragraph.get_text(separator=' ', strip=True)
                company_address.append(address)
                # print("Address:", address)
            else:
                print("Address paragraph not found")
        return company_address

    def get_news(self):
        url = f"{self.url}/blog/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_tag = soup.find('div', id='w-node-_8f876c74-ebcd-ac59-4a97-1b00f5b8371a-26dec1de')
        latest_news = []
        if div_tag:
            # Article title
            title = div_tag.find('h3', class_='larger-h3').get_text(strip=True)
            # print(title)
            # Article date
            date = div_tag.find_all('p')[2].get_text(strip=True)  # 3rd <p> tag for date
            # print(date)
            # Article summary and URL from the second <div>
            summary_div = div_tag.find_all('div')[1]
            summary = summary_div.find('p').get_text(strip=True)
            # print(summary)
            url = summary_div.find('a', class_='text-link')['href']
            # print(url)
            latest_news.append({'title': title,
                                'date': date,
                                'summary': summary,
                                'url': self.url + url})
        return latest_news

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        img_tags = soup.find_all('div', class_='client-logo')
        # Extract company names from image URLs
        # print(img_tags)
        company_names = []
        for img_tag in img_tags:
            src = img_tag.find('img')['src']
            # print(src)
            # Extract company name from URL
            match = re.search(r'/([^/]+)\.(?:png|jpg|jpeg|gif)', src)
            if match:
                company_name_match = match.group(1)
                # Decode URL encoding (e.g., %2520 to space)
                company_name_replace = company_name_match.replace('%2520', ' ').replace('%20', ' ')
                company_name = re.sub(r'\b(?:-Logo|-logo|Logo|logo)\b', '', company_name_replace).strip()
                company_names.append(company_name)

        # Cleaned company names
        company_names = [name.split('_')[-1].capitalize() for name in company_names]
        # print(company_names)
        return company_names
