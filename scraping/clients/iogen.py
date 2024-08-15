import time
from bs4 import BeautifulSoup
from base import Scrapping


class Iogen(Scrapping):
    def __init__(self, c_id, c_name, c_url, output_type, driver):
        super().__init__(c_id, c_name, c_url, output_type)
        self.driver = driver

    def get_description(self):
        url = f"{self.url}/company/"
        self.driver.get(url)
        # Optionally wait for content to load
        time.sleep(20)  # Wait 5 seconds for content to load

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        container_div = soup.find('div', class_='container column-1 Bxsh(n) Gc(2) Gr(1) m:Gc(1) m:Gr(2)')

        about_company = []
        if container_div:
            # Find the first <span> tag within the container_div
            first_span = container_div.find('span')

            if first_span:
                # Get the text of the first <span>
                company = first_span.get_text(separator=' ', strip=True)
                about_company.append(company)
            else:
                print("First span not found")
        else:
            print("Container div not found")
        if about_company:
            return about_company[0]
        else:
            return about_company

    def get_contacts(self):
        url = f"{self.url}/contact/"
        self.driver.get(url)

        time.sleep(20)

        # Extract the rendered page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        address_div = soup.find('div',
                                {'pagecloud-guid': '9768acb9-a0b2-4b10-da6a-d11161aac184', 'pagecloud-lm': 'desktop'})

        company_address = []
        if address_div:
            # Find the <span> tag within the <div>
            span_tag = address_div.find('span')
            if span_tag:
                # Extract the text from the <span> tag
                address_text = span_tag.get_text(separator=' ', strip=True)
                company_address.append(address_text)
            else:
                print("Address <span> tag not found")
        else:
            print("Address <div> tag not found")

        return company_address
