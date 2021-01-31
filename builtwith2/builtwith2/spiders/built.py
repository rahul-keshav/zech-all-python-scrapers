import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['www.bargainw.com']
    start_urls = ['https://www.bargainw.com/wholesale/1082/Wholesale-Products.html?sort=&size=5000&page=1&sortBy=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths= '//div[@class="product_name"]/a'), callback='parse_item_2', follow=True),
        )

    def parse_item_2(self, response):
        time.sleep(1)
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