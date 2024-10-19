from bs4 import BeautifulSoup
import requests
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
import re
import json

# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

urls = [
    #executive condos
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/eligibility",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/cpf-housing-grants",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/buying-procedures",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/application",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/conditions-after-buying-for-ec",
    #resale flats
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/overview",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-completion",
    #new flats
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/timeline",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/modes-of-sale",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/application",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/booking-of-flat",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/sign-agreement-for-lease",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/key-collection",
    "https://www.hdb.gov.sg/residential/buying-a-flat/conditions-after-buying",
    #housing loan options
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options",
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/flat-and-grant-eligibility",
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/housing-loan-options/housing-loan-from-hdb",
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/housing-loan-options/housing-loan-from-financial-institutions",
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/application-for-an-hdb-flat-eligibility-hfe-letter",
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/application-for-an-hdb-flat-eligibility-hfe-letter/income-guidelines",
    #finding a flat
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/finding-a-flat",
    #Conditions after buying
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/conditions-after-buying",
]

# Custom extractor function to extract text from HTML using BeautifulSoup
def custom_extractor_with_headers(url):
    # Make a request using the headers to mimic a browser
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None

# Function to create a valid key from the URL for storing data in a dictionary
def url_to_key(url):
    # Remove the protocol (http, https), www, and replace non-alphanumeric characters with underscores
    key = re.sub(r'[^a-zA-Z0-9]', '_', url)
    return key

# Dictionary to store the scraped data for each website
scraped_data = {}

# Loop through each URL and store the data in the dictionary
for i, url in enumerate(urls):
    # Use the custom extractor with headers
    page_content = custom_extractor_with_headers(url)
    
    # If the content was fetched successfully
    if page_content:
        # Create a unique key based on the URL to store the data
        key = url_to_key(url)
        
        # Instantiate the RecursiveUrlLoader and use the content fetched with custom headers
        loader = RecursiveUrlLoader(url=url, extractor=lambda x: page_content)
        
        # Load the data from the website
        docs = loader.load()
        
        # Store the data in the dictionary under the key
        scraped_data[key] = []
        
        # Loop through the documents and append them to the dictionary entry
        for doc in docs:
            title = doc.metadata.get("title")
            source = doc.metadata.get("source")
            content = doc.page_content
            
            # Ensure that the title, source, and content are string type
            if isinstance(title, str) and isinstance(source, str) and isinstance(content, str):
                scraped_data[key].append({
                    "title": title,
                    "source": source,
                    "content": content
                })
            else:
                print(f"Skipped a document from {url} due to non-string content.")
    else:
        print(f"Could not retrieve data from {url}")

with open('scraped_data_buyingflat.json', 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

# Now the scraped data is stored in the `scraped_data` dictionary and can be used later
print("Data scraping complete. You can now access the data from the `scraped_data` dictionary.")
print("Total documents loaded:", len(scraped_data))
print(scraped_data)
