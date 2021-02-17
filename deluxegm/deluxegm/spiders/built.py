import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

class BuiltSpider(scrapy.Spider):
    name = 'built'
    allowed_domains = ['www.deluxegm.com']
    start_urls = ['https://www.deluxegm.com/']

    def parse(self, response):
        urls = response.xpath('//a[@class="left-nav" or @class="left-nav-lrg"]/@href').getall()
        for url in urls:
            url = url+'&itemcount=500'
            yield response.follow(url = url, callback = self.parse_2)

    def parse_2(self,response):
        urls = response.xpath('//p[@class="prdct-desc"]/a/@href').getall()
        for url in urls:
            yield response.follow(url, callback = self.parse_item)    
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths= '//a[@class="left-nav" or @class="left-nav-lrg"]'), follow=True),
    #     Rule(LinkExtractor(restrict_xpaths= '//p[@class="prdct-desc"]/a'), callback='parse_item', follow=True),
    #     )

    def parse_item(self, response):
        title = response.xpath('//h1/text()').get()
        img = response.xpath('//div[@class="dtl-left"]/a/img/@src').get()
        image = 'https://www.deluxegm.com'+ img
        price = response.xpath('//span[@class="txtRedLarge"]/text()').get()
        description = response.xpath('//strong[text()="Description:"]/parent::node()/text()').get()
        more_detail = response.xpath('//strong[text()="More Details:"]/parent::node()/text()').get()
        item_no = response.xpath('//strong[text()="Item #:"]/parent::node()/text()').get()
        colors = response.xpath('//strong[text()="Colors:"]/parent::node()/text()').get()
        item_size = response.xpath('//strong[text()="Item Size:"]/parent::node()/text()').get()
        origin = response.xpath('//strong[text()="Origin:"]/parent::node()/text()').get()
        category = response.xpath('//strong[text()="Category:"]/parent::node()/a/text()').get()
        sub_category = response.xpath('//strong[text()="Sub-Category:"]/parent::node()/a/text()').get()        
        upc = response.xpath('//strong[text()="UPC:"]/parent::node()/text()').get()
        item_weight = response.xpath('//strong[text()="Item Weight:"]/parent::node()/text()').get()
        minimum_quantity = response.xpath('//strong[text()="Minimum Quantity:"]/parent::node()/text()').get()
        case_dimensions = response.xpath('//strong[text()="Case Dimensions:"]/parent::node()/text()').get()
        case_pack = response.xpath('//strong[text()="Case Pack:"]/parent::node()/text()').get()
        packed_in = response.xpath('//strong[text()="Packed In:"]/parent::node()/text()').get()
        inner_pack = response.xpath('//strong[text()="Inner Pack:"]/parent::node()/text()').get()
        case_weight = response.xpath('//strong[text()="Case Weight:"]/parent::node()/text()').get()
        case_cube = response.xpath('//strong[text()="Case Cube:"]/parent::node()/text()').get()

        yield{
            'title':title,
            'item_no':item_no,
            'image':image,
            'price':price,
            'description':description,
            'more_detail':more_detail,
            'colors':colors,
            'item_size':item_size,
            'origin':origin,
            'category':category,
            'sub_category':sub_category,
            'upc':upc,
            'packed_in':packed_in,
            'item_weight':item_weight,
            'minimum_quantity':minimum_quantity,
            'case_dimensions':case_dimensions,
            'case_pack':case_pack,
            'inner_pack':inner_pack,
            'case_weight':case_weight,
            'case_cube':case_cube,
            'url':response.url
        }
