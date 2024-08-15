import time
from bs4 import BeautifulSoup
from base import Scrapping


class HydrogeniousLOHC(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/who/#ambition/"
        self.driver.get(url)

        time.sleep(5)

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        about_us = []
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            about_us.append(paragraph.get_text(strip=True))

        data = " ".join(about_us[:3])
        return data

    def get_contacts(self):
        url = f"{self.url}/who/#contacts"
        self.driver.get(url)

        time.sleep(5)

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        office_data = []
        # Find all office sections by looking for <h3> tags
        office_sections = soup.find_all('div', class_='block text-size-m m-t-2')
        office_sections = office_sections[3]
        # print(office_sections)
        office1_name = office_sections.find('h3').get_text(separator=" ").strip()
        office1_address = office_sections.find_all('p')[1].get_text(separator=" ").strip()
        office_data.append(office1_address)
        # Extract the second office information
        office2_name = office_sections.find_all('h3')[1].get_text(separator=" ").strip()
        office2_address = office_sections.find_all('p')[4].get_text(separator=" ").strip()
        office_data.append(office2_address)
        return office_data

    def get_news(self):
        url = f"{self.url}/updates/#news"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        article = soup.find('article', class_='article--news')
        # print(latest_article)
        url1 = article.find('a', href=True)['href']
        # print(url1)
        title = article.find('h3').get_text(strip=True)
        date = article.find('div', class_='article__date').get_text(strip=True)
        latest_info = {
            'title': title,
            'date': date,
            'url': url1
        }

        # print(latest_info)
        self.driver.get(url1)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source1 = self.driver.page_source
        soup1 = BeautifulSoup(page_source1, 'html.parser')
        heading = soup1.find('h1').get_text(strip=True)
        paragraphs = soup1.find_all('p')
        paragraph_data = []
        for paragraph in paragraphs:
            paragraph_data.append(paragraph.get_text(strip=True))
        # content = paragraphs[0].get_text(strip=True)

        latest_info = {
            'title': title,
            'date': date,
            'url': url1,
            'content': heading
        }
        return [latest_info,]

    def get_clients(self):
        url = f"{self.url}/who/#contacts"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        logo_div = soup.find('div', class_='block-logo m-y-4')

        # List to store company names
        company_names = []

        # Check if the div was found
        if logo_div:
            # Find all img tags within the div
            for img_tag in logo_div.find_all('img'):
                # Extract the src attribute
                img_src = img_tag['src']

                # Extract the company name from the image source URL
                # The name is assumed to be between the last slash and the underscore
                company_name = img_src.split('/')[-1].split('_')[0]
                if '-' in company_name:
                    company_name = company_name.split('-')[1].split('.')[0]
                    # Add the company name to the list
                    company_names.append(company_name)
                else:
                    company_names.append(company_name)

        # Output the list of company names
        return company_names
