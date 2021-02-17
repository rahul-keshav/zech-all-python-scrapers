import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['www.hjcloseouts.com']
    start_urls = ['https://www.hjcloseouts.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[starts-with(@class,"cat-item")]/a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="product-detail-wrapper"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next page-numbers"]'), follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('normalize-space(//h1[@class="product_title entry-title"]/text())').get()
        image = response.xpath('//img[@class="wp-post-image"]/@src').get()
        upc = response.xpath('normalize-space(//span[@class="upc"]/text())').get()
        price = response.xpath('normalize-space(//p[@class="single_product_price_piece"]/span/text())').get()

        yield{
            'title':title,
            'image':image,
            'upc':upc,
            'price':price,
            'url':response.url
        }
