from helpers import read_json
import json

products = read_json('products.json')['data']

def contains_identifier_key(metadata: list):
    keys = [m['key'] for m in metadata]
    return 'identifier' in keys

products = [p for p in products if contains_identifier_key(p['metadata'])]

print(len(products))

print()
print()
print()

for product in products:
    print(product['search'])
    print()
    identifier_metadata = [m for m in product['metadata'] if m['key'] == 'identifier'][0]
    print('identifier:', identifier_metadata['value'])
    print()
    print('retailer:', product['retailerId'])
    print()
    print('-'*60)
    print()

quit()

metadatas = [p['metadata'] for p in products]
metadatas = [[m for m in metadata if m['key'] == 'identifier'][0]
    for metadata in metadatas]

for metadata in metadatas:
    print(metadata['value'])

# print(json.dumps(metadatas[2:12], indent=4))

# print(json.dumps(products[2:12], indent=4))