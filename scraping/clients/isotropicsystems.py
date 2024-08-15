import time
from bs4 import BeautifulSoup
from base import Scrapping


class IsotropicSystems(Scrapping):
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

        # Extract all <p> tag data
        p_tags = soup.find_all('p', class_='display-2')
        combined_text = ' '.join(p.get_text(strip=True) for p in p_tags)
        return combined_text

    def get_contacts(self):
        url = f"{self.url}/contact"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        locations = []

        # Find all divs with class col-md-3
        for location_div in soup.find_all('div', class_='col-md-3'):
            # Extract the heading and the paragraph text
            heading = location_div.find('h3').get_text(strip=True)
            paragraph = location_div.find('p').get_text(separator='  ', strip=True)
            locations.append(paragraph)
        return locations

    def get_news(self):
        url = f"{self.url}/insights"
        self.driver.get(url)

        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        articles = soup.find_all('div', class_='post-card')
        news = []
        latest_new = []
        # Extract the details
        for article in articles:
            # Extract title
            title_tag = article.find('h3', class_='display-3')
            title = title_tag.get_text(strip=True) if title_tag else 'No title'

            # Extract date
            date_tag = article.find('p', class_='display-4 mb-1 date regular')
            date = date_tag.get_text(strip=True).strip() if date_tag else 'No date'

            # Extract URL
            url_tag = article.find('a', class_='card-title-link')
            article_url = url_tag['href'] if url_tag and 'href' in url_tag.attrs else 'No URL'
            news.append({
                'Title': title,
                'Date': date,
                'URL': article_url})
        # print(news)
        self.driver.get(news[0]['URL'])

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        content_div = soup.find('div', class_='col-md-6 content')

        # Extract all <p> and <li> tag text within that div
        paragraphs = content_div.find_all('p')
        list_items = content_div.find_all('li')

        # Combine and print the text
        summary = ' '.join(para.get_text(strip=True) for para in paragraphs) + ' ' + ' '.join(
            item.get_text(strip=True) for item in list_items)

        news[0]["summary"] = summary
        latest_new.append(news[0])
        return latest_new
