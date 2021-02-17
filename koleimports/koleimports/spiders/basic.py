import json
import pprint
file = open('koleimports/spiders/category.json', 'r')
# file = open('category.json', 'r')
data = json.load(file)
list1 = data.get('data').get('topMenuInfo').get('list')
category = data.get('data').get('topMenuInfo').get('list')[0].get('special_category')
collection = data.get('data').get('topMenuInfo').get('list')[2].get('subcategory')


all_url = []
for cat in category:
    s_list = cat.get('category_info')
    for item in s_list:
        name = item.get('name')
        url = item.get('url')
        all_url.append(url)
for item in collection:
    name = item.get('name')
    url = item.get('url')
    all_url.append(url)


def id_extract(string):
    print(string)
    index_1 = string.find('category_id')
    index_2 = string.find('category_image')
    new_string = string[index_1:index_2] 
    cat_id = int(''.join(filter(str.isdigit, new_string)))    
    return(cat_id)

