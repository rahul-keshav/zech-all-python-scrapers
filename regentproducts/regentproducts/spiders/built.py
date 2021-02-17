import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['regentproducts.com']
    start_urls = ['https://regentproducts.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="graybg"]/a'),follow=True),
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="productListing-even" or @class="productListing-odd"]/td[3]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='(//a[@title=" Next Page "])[1]'),follow=True),


    )
    def image_correction(self,image_string):
        first_index = image_string.find("'")
        last_index = image_string.rfind("'")
        image = image_string[first_index+1:last_index]

        image_url = 'https://regentproducts.com/'+image
        return image_url

    def parse_item(self, response):
        
        title = response.xpath('normalize-space(//td[@class="pageHeading"][1]/text())').get().strip()
        price = response.xpath('normalize-space(//td[@class="pageHeading"][2]/text())').get().strip()
        image_link = response.xpath('//td[@class="main_table_heading_inner"]//td/script/text()').get()
        image_index = image_link.rfind('=')
        image = image_link[image_index+1:]
        image_url = self.image_correction(image)

        upc = response.xpath('//strong[text()="UPC: "]/parent::node()/text()').get()
        item_No = response.xpath('//strong[text()="Item #: "]/parent::node()/text()').get()
        quantity = response.xpath('//strong[text()="Quantity In Case Pack: "]/parent::node()/text()').get()
        desc = response.xpath('//p[@style="font-size:12px;"]/preceding-sibling::node()')
        description = desc[-1].xpath('.//text()').get()

        yield{
            'Title':title,
            'Price':price,
            'UPC':upc,
            'Item #':item_No,
            'Quantity In Case Pack':quantity,
            'Description':description,
            'image_url':image_url,
            'url':response.url
        }