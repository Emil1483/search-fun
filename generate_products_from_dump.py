from helpers import prettify, write_json


def dicts_from_sql(file, name):
    keys = []
    with open(file) as f:
        first = True
        for line in f:
            if not first and 'INSERT INTO' in line:
                continue

            csv = line.replace("(", "")
            csv = csv.replace(")", "")
            csv = csv.replace(f"INSERT INTO `{name}`", "")
            csv = csv.replace("VALUES", "")

            inside_quotes = False
            n = len(csv)
            for i, char in enumerate(csv[::-1]):
                index = n - i - 1
                if char == '"':
                    inside_quotes = not inside_quotes
                    continue

                if char == ',' and inside_quotes:
                    csv = csv[:index] + 'ÆØÅwegottheÆØÅ' + csv[index + 1:]

            csv = csv.replace('"', "")
            values = csv.split(",")
            values = [v.replace('ÆØÅwegottheÆØÅ', ",").strip() for v in values if len(v.strip()) > 0]

            if first:
                first = False
                keys.extend([v.replace('`', '') for v in values])
                continue

            result = {}
            for key, value in zip(keys, values):
                if value == 'NULL' or value == 'NULL;':
                    result[key] = None
                    continue

                result[key] = value

            yield result

retailers = [*dicts_from_sql('dump/newcycle-core.Retailer.00001.sql', 'Retailer')]

def dict_from_id(dicts, id):
    for d in dicts:
        if d['id'] == id:
            return d
    print(f'Could not find dict with id {id}')
    return None

products = []
for product in dicts_from_sql('dump/newcycle-core.Product.00001.sql', 'Product'):
    product['retailer'] = dict_from_id(retailers, product['retailerId'])
    product['metadata'] = []
    products.append(product)

print('done with products')

for i, meta_data in enumerate(dicts_from_sql('dump/newcycle-core.ProductMetadata.00001.sql', 'ProductMetadata')):
    product = dict_from_id(products, meta_data['productId'])
    if product is not None:
        product['metadata'].append(meta_data)
    if i % 1000 == 0: print(i)

write_json('products.json', products)