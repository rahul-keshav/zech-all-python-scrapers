import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['www.jcsalesweb.com']
    start_urls = ['https://www.jcsalesweb.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="nav-category-item"]/a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="display-label product-name"]/a'), callback = 'parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="page-nav-label"])[2]'), follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//h2/text()').get()
        item_no = response.xpath('normalize-space(//div[@style="margin-top: 4px; font-size: 17px; font-weight: bold; color: #103972;"]/text())').get()
        country_of_origin = response.xpath('normalize-space(//div[contains(text(),"Country of Origin")]/text())').get()
        barcode  = response.xpath('normalize-space(//div[contains(text(),"Barcode")]/text()[2])').get()
        desc = response.xpath('normalize-space(//div[@class="product-umdescription"]/text())').get()
        image = response.xpath('//div[@class="image"]/a[@class="dispaly-large-image"]/@href').get()
        price = response.xpath('normalize-space(//span[@class="display-label each-price"]/text())').get()
        pack_price = response.xpath('normalize-space(//span[@class="pack-price"]/text())').get()

        yield{
            'title':title,
            'item_no':item_no,
            "Country of Origin":country_of_origin,
            'barcode':barcode,
            'Description':desc,
            'image':image,
            'price':price,
            'pack_price':pack_price,
            'url':response.url
        }
