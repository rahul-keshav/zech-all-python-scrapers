import json
import pprint

file = open('item_detail.json', 'r')
data = json.load(file)
item = data.get('data').get('products').get('items')
item = item[0]

id = item.get('id') 
name = item.get('name')
sku = item.get('sku')
url_key = item.get('url_key')
special_price = item.get('special_price')
regularPrice = item.get('price').get('regularPrice').get('amount').get('value')

tier_prices = item.get('tier_prices')
t_p = [price.get('value') for price in tier_prices]
t_p_txt = [str(p) for p in t_p]
tier_price_txt = ','.join(t_p_txt)

categories = item.get('categories')
cat = [p['name'] for p in categories]
cat_text = ', '.join(cat)
status = item.get('stock_status')

description = item.get('description')
status = item.get('stock_status')
upc = item.get('upc')




print(id)