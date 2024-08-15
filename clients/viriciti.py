import time
from bs4 import BeautifulSoup
from base import Scrapping


class Viriciti(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = self.url
        self.driver.get(url)
        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        about_company = []
        div_tag = soup.find('div', class_='container container--override-width')

        # Extract the text content from all h3 tags within the div tag
        if div_tag:
            h3_tags = div_tag.find_all('h3')
            for h3 in h3_tags:
                about_company.append(h3.get_text(strip=True))
        data = " ".join(about_company)
        return data

    def get_clients(self):
        url = self.url
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_tag = soup.find('div', class_='marquee')

        company_names = []
        # If the div is found, extract data from it
        if div_tag:
            # Find all img tags within the div
            images = div_tag.find_all('img')

            # Extract company names from the alt attributes
            company_names = [img['alt'].replace(' logo', '') for img in images]

            # Print the extracted company names
            for name in company_names:
                print(name)
        else:
            print("Div tag not found")

        return company_names

    def get_contacts(self):
        url = f"{self.url}/about/contact"
        self.driver.get(url)

        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        main_div = soup.find('div', class_='col-sm-6')

        # Initialize a list to store the extracted data
        address_data = []

        # Find all the <h3> tags and their corresponding <p> tags
        sections = main_div.find_all(['h3', 'p'])

        current_heading = None
        for section in sections:
            if section.name == 'h3':
                # Save the current heading for grouping the following paragraphs
                current_heading = section.get_text(strip=True)
            elif section.name == 'p' and current_heading:
                # Extract the text within the <p> tag
                address = section.get_text(separator=" ", strip=True)
                # Append the data to the list
                address_data.append(address)
        return address_data

    def get_news(self):
        url = f"{self.url}/about/media"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        news = []
        articles = soup.find_all('div', class_='col-sm-4 mb20')

        # Extract and print the title, URL, and date for each article
        for article in articles:
            # Find the link tag within the article
            link_tag = article.find_all('a')
            # print(link_tag)

            for link in link_tag:
                # print(link)
                url1 = link['href']
                # print(url)
                # Find the strong tag for the title
                title_tag = link.find_all('strong')
                # print(title_tag)
                title = ""
                for title in title_tag:
                    title = title.get_text(strip=True)
                    # print(title)
                # Find the date tag
                date_tag = article.find('time')
                date = date_tag.get_text(strip=True) if date_tag else 'No date available'

                news.append({
                    'title': title,
                    'date': date,
                    'url': self.url + url1
                })
        url2 = news[0]['url']
        self.driver.get(url2)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        div_tag = soup.find('div',
                            class_='paragraph paragraph--type--paragraph-text paragraph--view-mode--default')

        # Extract the first two paragraphs
        paragraphs = div_tag.find_all('p', limit=2)

        # Combine the text from each paragraph into a single string
        summary = ' '.join(para.get_text(strip=True) for para in paragraphs)
        latest_news = [{
            'title': news[0]['title'],
            'date': news[0]['date'],
            'url': news[0]['url'],
            'summary': summary
        }]
        return latest_news
