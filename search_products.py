import os
from algoliasearch.search_client import SearchClient

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')

client = SearchClient.create(APP_ID, API_KEY)
index = client.init_index("products")

results = index.search("musematte")

for hit in results["hits"]:
    name = hit["name"]
    retailer_name = hit["retailer"]["name"]
    # print(prettify(hit))
    # print()
    print("name:", name)
    print("retailer_name:", retailer_name)
    input()
    # print()