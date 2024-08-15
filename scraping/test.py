#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless mode, without opening a browser window
#service = Service(
#    executable_path='/opt/homebrew/Caskroom/chromedriver/127.0.6533.99/chromedriver-mac-arm64/chromedriver')  # Replace with the actual path to your chromedriver
service = Service(executable_path=r'chromedriver-win64\chromedriver.exe')

driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.iogen.com"
driver.get(url)

# Optionally wait for content to load
time.sleep(5)  # Wait 5 seconds for content to load

# Extract the rendered page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')



urls = []
keys = ["Our Technology", "Contact", "Company"]
urls_dict = {}
for key in keys:
    anchor_tags = soup.find_all('a', href=True)
    # print(anchor_tags)
    for anchor_tag in anchor_tags:
        if key in anchor_tag.get_text(strip=True):
            # print(anchor_tag.get_text(strip=True))
            base_url = url + anchor_tag['href']
            urls.append({key: base_url})
            # urls_dict[key] = anchor_tag['href']
            break  # Stop after finding the fi

# In[2]:


urls

# In[4]:




url = "https://www.iogen.com/company"
driver.get(url)

# Optionally wait for content to load
time.sleep(20)  # Wait 5 seconds for content to load

# Extract the rendered page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')



# In[7]:


container_div = soup.find('div', class_='container column-1 Bxsh(n) Gc(2) Gr(1) m:Gc(1) m:Gr(2)')

about_company = []
if container_div:
    # Find the first <span> tag within the container_div
    first_span = container_div.find('span')

    if first_span:
        # Get the text of the first <span>
        company = first_span.get_text(separator=' ', strip=True)
        about_company.append(company)
        print("About Company:", company)
    else:
        print("First span not found")
else:
    print("Container div not found")




url = "https://www.iogen.com/iogen-technology"
driver.get(url)

# Optionally wait for content to load
time.sleep(20)  # Wait 5 seconds for content to load

# Extract the rendered page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')


# In[14]:


content_p = soup.find('p', {'data-alt-style': 'line-height: 1.5; text-align: justify;'})

if content_p:
    # Extract the text from the <p> tag, including text from nested <span> tags
    company_technology = content_p.get_text(separator=' ', strip=True)
    print("Extracted Text:", company_technology)
else:
    print("Content <p> tag not found")

# In[15]:





url = "https://www.iogen.com/contact"
driver.get(url)

# Optionally wait for content to load
time.sleep(20)  # Wait 5 seconds for content to load

# Extract the rendered page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')



# In[18]:


address_div = soup.find('div', {'pagecloud-guid': '9768acb9-a0b2-4b10-da6a-d11161aac184', 'pagecloud-lm': 'desktop'})

company_address = []
if address_div:
    # Find the <span> tag within the <div>
    span_tag = address_div.find('span')
    if span_tag:
        # Extract the text from the <span> tag
        address_text = span_tag.get_text(separator=' ', strip=True)
        company_address.append(address_text)
        print("Extracted Address:", address_text)
    else:
        print("Address <span> tag not found")
else:
    print("Address <div> tag not found")

# In[ ]:




