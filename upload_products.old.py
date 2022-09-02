import os
from helpers import read_json
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

load_dotenv()

retailers = read_json('retailers.json')['Retailer']

def retailer_from_id(id):
    for retailer in retailers:
        if retailer['id'] == id:
            return retailer
    raise ValueError(f'Could not find retailer with id {id}')

products = read_json('products.json')['Product']
for product in products:
    product['retailer'] = retailer_from_id(product['retailerId'])
    product['objectID'] = product['id']
    del product['id']

# for product in products:
#     print(prettyfy(product))
#     input()


APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')

client = SearchClient.create(APP_ID, API_KEY)
index = client.init_index('products')

index.save_objects(products).wait()