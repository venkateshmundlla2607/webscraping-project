import time
from bs4 import BeautifulSoup
from base import Scrapping


class BioBTX(Scrapping):
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
        about_us = []
        div_content = soup.find('div', class_='col-12 col-lg-8 offset-lg-2')
        # Extract the second paragraph text from the div
        about_us.append(div_content.find_all('p')[1].get_text(strip=True))
        data = " ".join(about_us)
        return data

    def get_news(self):
        url = f"{self.url}/news/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        blog_posts = soup.find_all('div', class_='blog-post')
        news = []
        for post in blog_posts:
            title = post.find('h2', class_='entry-title').text.strip()
            date = post.find('p', class_='date').text.strip()
            link = post.find('a')['href']

            if len(news) == 0:
                news.append({
                    'title': title,
                    'date': date,
                    'link': link})
        url1 = news[0]['link']
        self.driver.get(url1)
        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source1 = self.driver.page_source
        soup1 = BeautifulSoup(page_source1, 'html.parser')
        summary = soup1.find('h2').get_text(separator=" ")
        news.append({
            'summary': summary})
        return news

    def get_clients(self):
        url = f"{self.url}/partners/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        company_names = []
        for a_tag in soup.select('.row .blog-column a'):
            href = a_tag['href']
            # Extracting the domain name from the href link
            domain = href.split('//')[-1].split('/')[0]
            # Removing "www." and the domain extensions (.nl, .eu, etc.)
            company_name = domain.replace('www.', '').split('.')[0]
            company_name = company_name.capitalize()
            company_names.append(company_name)
        return company_names
