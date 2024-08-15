import time
from bs4 import BeautifulSoup
from base import Scrapping


class CharmIndustrial(Scrapping):
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
        target_div = soup.find('div', class_="flex flex-col w-full items-center text-center")
        # about_company = []
        # Extract the h2 and span tags within that div
        h2_text = target_div.find('h2').get_text(strip=True)
        span_text = target_div.find('span').get_text(strip=True)
        # Combine the texts into one string
        about_company = f"{h2_text} {span_text}"
        return about_company

    def get_clients(self):
        url = self.url
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div', class_='flex w-max animate-horizontal-scroll flex-nowrap items-center gap-16 whitespace-pre-line')
        company_names = []
        # Extract company names from the alt attributes of img tags within that div
        companies = [img['alt'] for img in target_div.find_all('img')]
        for company in companies:
            if company not in company_names:
                company_names.append(company)
        return company_names

    def get_news(self):
        url = f"{self.url}/press/"
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div', class_='space-y-6 text-charm-dark lg:grid lg:grid-cols-3 lg:gap-6 lg:space-y-0')
        # Find all <a> tags inside this <div>
        links = target_div.find_all('a')
        # Extract titles and URLs
        news = []
        for link in links:
            aria_label = link.get('aria-label', '')
            url = link.get('href', '')
            # Extract the title from aria-label
            title_start = aria_label.find('\'') + 1
            title_end = aria_label.find('\'', title_start)
            title = aria_label[title_start:title_end]
            news.append({
                'title': title,
                'url': url
                 })
        url = news[0]['url']
        self.driver.get(url)
        time.sleep(5)  # Wait 5 seconds for content to load
        # Extract the rendered page source
        page_source = self.driver.page_source
        soup1 = BeautifulSoup(page_source, 'html.parser')
        latest_news = []
        latest_news.append(news[0])
        widget_body_div = soup1.find('div', class_='widget__body clearfix sm-mt-1')
        # Extract the summary from the <p> tag inside widget__subheadline
        summary_p = widget_body_div.find('div', class_='widget__subheadline').find('p')
        summary = summary_p.get_text(strip=True) if summary_p else 'No summary found'
        # Extract the date from the <div class="post-date">
        post_date_div = widget_body_div.find('div', class_='post-date')
        date = post_date_div.get_text(strip=True) if post_date_div else 'No date found'
        latest_news[0]['date'] = date
        latest_news[0]['summary'] = summary
        return latest_news
