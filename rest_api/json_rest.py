import json
import pprint

with open('json.json','r') as file:
    data = json.load(file)

    # json.loads() this takes string as a input

# print(data)
printer = pprint.PrettyPrinter()
# printer.pprint(data)
# print(data.keys())
alldata = data.get('data')
products = alldata.get('products')
print(products.keys())
items = products.get('items')
printer.pprint(items)