import scrapy
import json
from .basic import all_url,id_extract
import requests

class BuiltSpider(scrapy.Spider):
    name = 'built'
    allowed_domains = ['www.koleimports.com']
    def start_requests(self):
        for url in all_url:
            yield scrapy.Request(url=url, callback= self.start_requests_2)

    def start_requests_2(self,response):
        category_id_string = response.xpath('/html/body/script[2]').get()
        category_id = id_extract(category_id_string)
        for i in range(1,11):
            url = 'https://www.koleimports.com/graphql?query=query%20getProducts(%24search%3A%20String%2C%20%24filter%3A%20ProductAttributeFilterInput!%2C%20%24pageSize%3A%20Int!%2C%20%24currentPage%3A%20Int!%2C%20%24sort%3A%20ProductAttributeSortInput!%2C%20%24global_category_id%3A%20Int!)%20%7B%0A%20%20products(search%3A%20%24search%2C%20filter%3A%20%24filter%2C%20pageSize%3A%20%24pageSize%2C%20currentPage%3A%20%24currentPage%2C%20sort%3A%20%24sort%2C%20global_category_id%3A%20%24global_category_id)%20%7B%0A%20%20%20%20aggregations%20%7B%0A%20%20%20%20%20%20attribute_code%0A%20%20%20%20%20%20label%0A%20%20%20%20%20%20options%20%7B%0A%20%20%20%20%20%20%20%20count%0A%20%20%20%20%20%20%20%20label%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20url_param%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%20%20items%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20sku%0A%20%20%20%20%20%20type_id%0A%20%20%20%20%20%20url_key%0A%20%20%20%20%20%20small_image%20%7B%0A%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20price%20%7B%0A%20%20%20%20%20%20%20%20regularPrice%20%7B%0A%20%20%20%20%20%20%20%20%20%20amount%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20special_price%0A%20%20%20%20%20%20tier_prices%20%7B%0A%20%20%20%20%20%20%20%20customer_group_id%0A%20%20%20%20%20%20%20%20qty%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20categories%20%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20link_data%20%7B%0A%20%20%20%20%20%20%20%20link_price%0A%20%20%20%20%20%20%20%20link_minimum_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20stock_status%0A%20%20%20%20%20%20special_options%0A%20%20%20%20%20%20special_value%20%7B%0A%20%20%20%20%20%20%20%20closeout%0A%20%20%20%20%20%20%20%20new_item%0A%20%20%20%20%20%20%20%20special%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20pricing_model%0A%20%20%20%20%20%20min_qty%0A%20%20%20%20%20%20limit_status%0A%20%20%20%20%20%20minimum_order_qty%0A%20%20%20%20%20%20inner_pk_qty%0A%20%20%20%20%20%20case_pk_qty%0A%20%20%20%20%20%20item_info%20%7B%0A%20%20%20%20%20%20%20%20case_qty%0A%20%20%20%20%20%20%20%20inner_qty%0A%20%20%20%20%20%20%20%20input_qty%0A%20%20%20%20%20%20%20%20minimum%0A%20%20%20%20%20%20%20%20pricing_model%0A%20%20%20%20%20%20%20%20qty%0A%20%20%20%20%20%20%20%20qty_increment%0A%20%20%20%20%20%20%20%20is_saleable%0A%20%20%20%20%20%20%20%20tier_max_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20deal_info%20%7B%0A%20%20%20%20%20%20%20%20datetime_from%0A%20%20%20%20%20%20%20%20datetime_to%0A%20%20%20%20%20%20%20%20deal_price%0A%20%20%20%20%20%20%20%20deal_qty%0A%20%20%20%20%20%20%20%20min_order_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20special_from_date%0A%20%20%20%20%20%20special_to_date%0A%20%20%20%20%7D%0A%20%20%20%20page_info%20%7B%0A%20%20%20%20%20%20current_page%0A%20%20%20%20%20%20page_size%0A%20%20%20%20%20%20total_pages%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A&operationName=getProducts&variables=%7B%22filter%22%3A%7B%22category_id%22%3A%7B%22eq%22%3A%22{1}%22%7D%7D%2C%22sort%22%3A%7B%22position%22%3A%22ASC%22%7D%2C%22pageSize%22%3A24%2C%22currentPage%22%3A{0}%2C%22global_category_id%22%3A%22{1}%22%7D'.format(i,category_id)

            yield scrapy.Request(url= url, callback= self.parse_id)

    def parse_id(self, response):
        data = json.loads(response.body)

        items  = data.get('data').get('products').get('items')
        for item in items:
            sku = item.get('sku')
            image = item.get('small_image').get('url')         
            yield scrapy.Request(url = 'https://www.koleimports.com/graphql?query=query%20getProduct(%24filter%3A%20ProductAttributeFilterInput!%2C%20%24link_code%3A%20String)%20%7B%0A%20%20products(filter%3A%20%24filter%2C%20link_code%3A%20%24link_code)%20%7B%0A%20%20%20%20items%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20sku%0A%20%20%20%20%20%20type_id%0A%20%20%20%20%20%20url_key%0A%20%20%20%20%20%20media_gallery_entries%20%7B%0A%20%20%20%20%20%20%20%20image%20%7B%0A%20%20%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20thumbnail%20%7B%0A%20%20%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20price%20%7B%0A%20%20%20%20%20%20%20%20regularPrice%20%7B%0A%20%20%20%20%20%20%20%20%20%20amount%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20special_price%0A%20%20%20%20%20%20tier_prices%20%7B%0A%20%20%20%20%20%20%20%20customer_group_id%0A%20%20%20%20%20%20%20%20qty%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20categories%20%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20link_data%20%7B%0A%20%20%20%20%20%20%20%20link_price%0A%20%20%20%20%20%20%20%20link_minimum_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20description%20%7B%0A%20%20%20%20%20%20%20%20html%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20stock_status%0A%20%20%20%20%20%20special_options%0A%20%20%20%20%20%20special_value%20%7B%0A%20%20%20%20%20%20%20%20closeout%0A%20%20%20%20%20%20%20%20new_item%0A%20%20%20%20%20%20%20%20special%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20pricing_model%0A%20%20%20%20%20%20min_qty%0A%20%20%20%20%20%20limit_status%0A%20%20%20%20%20%20minimum_order_qty%0A%20%20%20%20%20%20inner_pk_qty%0A%20%20%20%20%20%20case_pk_qty%0A%20%20%20%20%20%20upc%0A%20%20%20%20%20%20case_pk_dimensions%0A%20%20%20%20%20%20weight%0A%20%20%20%20%20%20cube_inches%0A%20%20%20%20%20%20item_info%20%7B%0A%20%20%20%20%20%20%20%20case_qty%0A%20%20%20%20%20%20%20%20inner_qty%0A%20%20%20%20%20%20%20%20input_qty%0A%20%20%20%20%20%20%20%20minimum%0A%20%20%20%20%20%20%20%20pricing_model%0A%20%20%20%20%20%20%20%20qty%0A%20%20%20%20%20%20%20%20qty_increment%0A%20%20%20%20%20%20%20%20is_saleable%0A%20%20%20%20%20%20%20%20tier_max_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20specifications%20%7B%0A%20%20%20%20%20%20%20%20specifications_info%20%7B%0A%20%20%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20%20%20special_cats%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20prop_65%20%7B%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20content%0A%20%20%20%20%20%20%20%20icon_url%0A%20%20%20%20%20%20%20%20is_enable%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20deal_info%20%7B%0A%20%20%20%20%20%20%20%20datetime_from%0A%20%20%20%20%20%20%20%20datetime_to%0A%20%20%20%20%20%20%20%20deal_price%0A%20%20%20%20%20%20%20%20deal_qty%0A%20%20%20%20%20%20%20%20min_order_qty%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20special_from_date%0A%20%20%20%20%20%20special_to_date%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A&operationName=getProduct&variables=%7B%22filter%22%3A%7B%22sku%22%3A%7B%22eq%22%3A%22{0}%22%7D%7D%7D'.format(sku) , callback= self.parse, meta = {'image':image})
    
    
    def parse(self, response):
        data = json.loads(response.body)
 
        items  = data.get('data').get('products').get('items')
        item = items[0]
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
        image = response.meta['image']

        if special_price:
            t_p.append(special_price)
        if regularPrice:
            t_p.append(regularPrice)

        min_price = min(t_p)

        categories = item.get('categories')
        cat = [p['name'] for p in categories]
        cat_text = ', '.join(cat)
        description = item.get('description').get('html')
        status = item.get('stock_status')
        upc = item.get('upc')



        yield{
                'id':id,
                'name':name,
                'sku':sku,
                'upc':upc,
                'url_key':url_key,
                'image':image,
                'description':description,
                'special_price':special_price,
                'regular_price':regularPrice,
                'tier_prices':tier_price_txt,
                'min price':min_price,
                'categories':cat_text,
                'status':status,
                
            }
