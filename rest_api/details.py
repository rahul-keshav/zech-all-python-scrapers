import json
import pprint

file = open('details.json', 'r')
data = json.load(file)
items  = data.get('data').get('products').get('items')
for item in items:
    id = item.get('id')
    name = item.get('name')
    sku = item.get('sku')
    url_key = item.get('url_key')
    image = item.get('small_image').get('url')
    spacail_price = item.get('special_price')
    regular_price = item.get('price').get('regularPrice').get('amount').get('value')
    tier_prices = item.get('tier_prices')
    t_p = [price.get('value') for price in tier_prices]
    t_p_txt = [str(p) for p in t_p]
    tier_price_txt = ','.join(t_p_txt) 

    categories = item.get('categories')
    cat = [p['name'] for p in categories]
    cat_text = ', '.join(cat)
    status = item.get('stock_status')
    print(id)
    print(name)
    print(sku)
    print(url_key)
    print(image)
    print('spacail_price',spacail_price)
    print('regular_price',regular_price)
    print('tier_price',tier_price_txt)
    if len(t_p):
        min_price = min(t_p)
        print('min price',min_price)
    print('category =',cat_text)
    print(status)
    print()


# print(items)