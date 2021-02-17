import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['www.dollaritemdirect.com']
    start_urls = ["https://www.dollaritemdirect.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths= '//ul[@class="module-list cat-nav"]//a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths= '//td[@style="text-align:left;text-decoration:underline;text-transform:uppercase;"]/a'), callback='parse_details', follow=True),
        Rule(LinkExtractor(restrict_xpaths= '(//a[@class="pager-item-next"])[2]'), follow=True),
        )
    def upc_avail(self,string):
        index = string.rfind('UPC Coded:')
        if index<0:
            upc = ''
            return upc
        else:
            new_string = string[index:]
            comma_index = new_string.find(',')
            upc = new_string[:comma_index]
            return upc

    def upc_code(self,string):
        if string == '' or string == 'UPC Coded: No' or string == 'UPC Coded: Yes':
            return ''
        else:
            index = string.rfind(':')
            code = string[index+1:]
            return code.strip()

    def min_price(self,string):
        equal_index = string.rfind('=')
        if equal_index<0:
            price = string.strip(',')
            return price
        mul_index = string.find('x')
        return string[:mul_index]


    def parse_details(self, response):
        title = response.xpath('//div[@class="center_block_1"]/h2/span/text()').get()
        price_list = response.xpath('//span[@class="prod-detail-cost-value"]//text()').getall()
        prices = ','.join(price_list)
        if len(price_list)>0:                  
            minimum_price = self.min_price(price_list[-1])
        else:
            minimum_price = ''
        # minimum_price = self.min_price(price_list[-1])
        
        description_list = response.xpath('//div[@class="prod-detail-desc"]')
        all_description = description_list.xpath('.//text()').getall()
        descriptions = ', '.join(all_description)
        descriptions = descriptions.strip()
        descriptions = descriptions.replace('\t',' ')
        upc = self.upc_avail(descriptions)
        # upc_code = self.upc_code(upc)
        image = 'www.dollaritemdirect.com'+response.xpath('//div[@style="margin-bottom:10px"]/a/@href').get()
        yield{
            'title':title,
            'price':prices,
            'minimum price':minimum_price,
            'upc':upc,
            'descriptions':descriptions,
            'image':image,
            'url':response.url,
        }
        
