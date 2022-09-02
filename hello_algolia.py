import os
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')

client = SearchClient.create(APP_ID, API_KEY)

index = client.init_index("products")
record = {"objectID": 1, "name": "test_record"}
index.save_object(record).wait()

results = index.search("test_record")
print(results)