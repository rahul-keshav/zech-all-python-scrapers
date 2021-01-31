import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_selenium import SeleniumRequest
import time

class BuiltSpider(scrapy.Spider):
    name = 'built3'
    allowed_domains = ['www.bargainw.com']
    def start_requests(self):
        url = 'https://www.bargainw.com/wholesale/1082/Wholesale-Products.html?sort=&size=24&page=1&sortBy='
        yield SeleniumRequest(
            url=url,
            wait_time= 3,
            callback=self.parse,
        ) 

    def parse(self,response):
        product_link = response.xpath('//div[@class="product_name"]/a/@href').getall()
        next_page = response.xpath('(//a[@class="pageNavLink pageNavNext"])[2]/@href').get()
        print(next_page)
        for product in product_link:
            product_url = response.urljoin(product)
            yield SeleniumRequest(
                url = product_url,
                callback=self.parse_item_2
            )
        if next_page:
            print('following')
            yield SeleniumRequest(url=next_page,callback=self.parse) 

    def parse_item_2(self, response):
        title = response.xpath('//div[@class="details_cateory_name"]/text()').get().strip()        
        sku = response.xpath('(//td[@class="pv-5 pr-30" and @style="border-right: 0px solid #ccc;"])[1]/text()').get().strip()
        case_pack = response.xpath('//span[@class="casepack_value"]/text()').get().strip()
        UPC_no = response.xpath('//span[@class="upc_value"]/text()').get().strip()
        image_path = response.xpath('//img[@class="cloudzoom img-responsive center-block"]/@src').get()  
        image = 'https://www.bargainw.com'+str(image_path)
        price_each = response.xpath('normalize-space((//span[@class="price_value"])[1]/text())').get()
        price_case = response.xpath('normalize-space((//span[@class="price_value"])[2]/text())').get()
        short_description = response.xpath('//div[@class="details_short_desc"]/text()').get()
        if short_description:
            short_description = short_description.strip()
        else:
            short_description = ''
        spec_title = response.xpath('//div[@class="spec_title"]/text()').getall()
        spec_title = [i.strip() for i in spec_title]
        spec_info = response.xpath('//div[@class="spec_info"]/text()').getall()
        spec_info = [i.strip() for i in spec_info]
        spec = zip(spec_title,spec_info)
        spec_details = dict(spec)

        yield{
            'title':title,
            'sku':sku,
            'case_pack':case_pack,
            'UPC_no':UPC_no,
            'image':image,
            'price_each':price_each,
            'price_case':price_case,
            'short_description':short_description,
            'spec_details':spec_details,
            'url':response.url,
            
        }