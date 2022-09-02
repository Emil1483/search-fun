import os
from formatted_products import formatted_products
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

load_dotenv()

def products_formatted_for_angolia():
    for product in formatted_products():
        product['objectID'] = product['id']
        del product['id']

        yield product

products = [*products_formatted_for_angolia()]

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')

client = SearchClient.create(APP_ID, API_KEY)
index = client.init_index('products')
index.save_objects(products).wait()