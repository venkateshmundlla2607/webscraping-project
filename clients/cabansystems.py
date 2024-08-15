import time
from bs4 import BeautifulSoup
from base import Scrapping


class CabanSystems(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/about"
        self.driver.get(url)

        time.sleep(5)

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        section = soup.find('div', class_='section-default bg-is-beige')

        # Extract all p tags within this section
        all_ps = section.find_all('p')
        about_us = []
        for p in all_ps:
            about_us.append(p.text)
        return " ".join(about_us)

    def get_contacts(self):
        url = f"{self.url}/contact"
        self.driver.get(url)

        time.sleep(5)

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        location_divs = soup.find_all('div', class_='col-stretch is-locations')
        locations = []

        for div in location_divs:
            header = div.find('div', class_='para-large text-is-semi-bold')
            if header:
                header_text = header.get_text(strip=True)
                location_details = div.get_text(separator=' ', strip=True)
                # Remove the header from the details
                location_details = location_details.replace(header_text, '').strip()
                locations.append(location_details)
        return locations

    def get_clients(self):
        url = self.url
        self.driver.get(url)

        time.sleep(5)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        images = soup.find_all('img', class_='marquee_logo')

        alt_tags = set(img['alt'].replace(' logo', '') for img in images)
        companies = list(sorted(list(alt_tags)))
        return companies

    def get_news(self):
        url = f"{self.url}/resources"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        article_titles = []
        article_dates = []
        article_urls = []
        news = []
        latest_new = []
        # Loop through each article block
        for item in soup.find_all('div', class_='w-dyn-item'):
            # Find and store the title
            title_tag = item.find('p', class_='para-small')
            title = title_tag.text if title_tag else None

            # If the title is not found, skip this entry
            if not title:
                continue

            # Find and store the date
            date_tag = item.find('p', class_='para-xsmall')
            date = date_tag.text if date_tag else 'No date found'

            # Find and store the URL
            url_tag = item.find('a', class_='resource-block-child')
            url = url_tag['href'] if url_tag and 'href' in url_tag.attrs else 'No URL found'

            # If the URL is relative, prepend the base URL
            if url and not url.startswith('http'):
                url = self.url + url

            # Append the data to the lists
            article_titles.append(title)
            article_dates.append(date)
            article_urls.append(url)
            news.append({"title": title,
                         "date": date,
                         "url": url})

        # # Display the scraped data
        # for title, date, url in zip(article_titles, article_dates, article_urls):
        #     print(f"Title: {title}\nDate: {date}\nURL: {url}\n")
        self.driver.get(news[0]['url'])

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        paragraphs = soup.find_all('p')
        summary = []
        # Iterate through and print each paragraph's text
        for para in paragraphs:
            summary.append(para.get_text())
        news[0]["summary"] = summary[2]
        latest_new.append(news[0])
        return latest_new
