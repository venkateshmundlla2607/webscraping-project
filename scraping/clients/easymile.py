import time
from bs4 import BeautifulSoup
from base import Scrapping


class EasyMile(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/about-us"
        self.driver.get(url)
        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        about_company = []
        p_tags = soup.select('div.part-right p')
        # Extract the text from the first 3 <p> tags
        first_three_paragraphs = [p.get_text(strip=True) for p in p_tags[:3]]
        data = " ".join(first_three_paragraphs)
        return data

    def get_contacts(self):
        url = f"{self.url}/contact"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        contacts = []

        # Find all group-row divs
        for group in soup.find_all('div', class_='group-row'):
            # Get the region name from the h3 tag
            region_name = group.find('h3').get_text(strip=True)

            for content_div in group.find_all('div', class_='thecontent'):
                address = content_div.get_text(separator=' ', strip=True)
                contacts.append(address)
        return contacts

    def get_news(self):
        url = f"{self.url}/news"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        news_items = []
        for block in soup.select('div.blocklink.wow.views-row'):
            title_tag = block.select_one('div.views-field-title a')
            date_tag = block.select_one('div.views-field-created span')
            summary_tag = block.select_one('div.views-field-field-news-intro div.field-content')
            url1 = title_tag['href'] if title_tag else None
            title = title_tag.get_text(strip=True) if title_tag else None
            date = date_tag.get_text(strip=True) if date_tag else None
            # summary = summary_tag.get_text(strip=True) if summary_tag else None
            news_items.append({
                'title': title,
                'date': date,
                'url': self.url + url1
            })

        url2 = news_items[0]['url']

        self.driver.get(url2)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        latest_news = []

        div_tag = soup.find('div', class_='news-intro')

        latest_news.append({
            'title': news_items[0]['title'],
            'date': news_items[0]['date'],
            'url': news_items[0]['url'],
            'summary': div_tag.get_text(strip=True)
        })
        return latest_news
