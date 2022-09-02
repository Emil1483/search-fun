from math import prod
from helpers import prettify, read_json

def formatted_products():
    products = read_json('products.json')
    for product in products:
        del product['search']

        retailer = product['retailer']
        del product['retailer']

        def value_from_metadata(key):
            value_metadata = next((p for p in product['metadata'] if p['key'] == key), None)
            return value_metadata['value'] if value_metadata else None

        ean = value_from_metadata('ean')
        sku = value_from_metadata('sku') or value_from_metadata('varenummer')
        id_by_manufacturer = value_from_metadata('manufacturer_part_numbers')

        product['idByManufacturer'] = id_by_manufacturer
        product['ean'] = ean
        retailer['productSku'] = sku
        product['retailers'] = [retailer]

        del product['metadata']

        yield product

if __name__ == '__main__':
    for product in formatted_products():
        # if product['retailers'][0]['name'] != 'Elkjøp': continue
        # if product['retailers'][0]['productSku'] != '200744': continue
        print(prettify(product))
        input()