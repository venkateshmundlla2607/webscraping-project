import time
from bs4 import BeautifulSoup
from base import Scrapping


class EverStream(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/company/about-everstream/"
        self.driver.get(url)
        time.sleep(5)
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        about_company = []
        banner_description = soup.find('div', class_='page-banner-description')
        text = banner_description.find('p').get_text(strip=True)
        return text

    def get_contacts(self):
        url = f"{self.url}/company/contact-us/"
        self.driver.get(url)

        time.sleep(5)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_tags = soup.find_all('div', class_='contact-info-row')
        address = []
        p_text = ""
        if div_tags:
            last_div_tag = div_tags[-1]
            p_tag = last_div_tag.find('p', class_='contact-info-row-text')
            if p_tag:
                p_text = p_tag.get_text(strip=True)
            else:
                p_text = 'No <p> tag found'
        else:
            p_text = 'No <div> tags found'
        address.append(p_text)
        return address

    def get_clients(self):
        url = f"{self.url}/homepage/partners/"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        from urllib.parse import urlparse

        links = soup.find_all('a', class_='partner-logo-rows-image-link')

        # Function to extract and clean company names from URLs
        def extract_company_name(url):
            hostname = urlparse(url).hostname
            # Handle common TLDs and subdomains
            if hostname:
                parts = hostname.split('.')
                if len(parts) > 2:
                    return ' '.join(parts[1:-1]).replace('-', ' ').title()  # Join middle parts and format
                return parts[0].title()
            return 'Unknown'

        # Extract company names
        company_names = [extract_company_name(link['href']) for link in links]
        return company_names

    def get_news(self):
        url = f"{self.url}/insights/blog/"
        self.driver.get(url)

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        risk_cards = soup.find_all('div', class_='risk-card-bottom')

        # List to store the extracted data
        articles = []
        latest_article = []
        # Loop through all risk cards and extract the relevant information
        for card in risk_cards:
            title = card.find('h3', class_='risk-card-title').text.strip()
            date = card.find('p', class_='risk-card-date').text.strip()
            description = card.find('p', class_='risk-card-desc').text.strip()
            link = card.find('a', class_='carousel-link-wrapper')['href']
            # image = card.find_previous('img', class_='risk-card-asset')['src']

            # Append the extracted information as a dictionary to the articles list
            articles.append({
                'title': title,
                'date': date,
                'description': description,
                'link': link
            })

        self.driver.get(articles[0]['link'])

        # Optionally wait for content to load
        time.sleep(5)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        summary_tag = soup.find('div', class_='article-text-container').find_all('p')[0]

        # Extract and print the text
        summary = summary_tag.get_text(strip=True)
        latest_article.append({
            'title': articles[0]['title'],
            'date': articles[0]['date'],
            'description': articles[0]['description'],
            'url': articles[0]['link'],
            'summary': summary
        })
        return latest_article
