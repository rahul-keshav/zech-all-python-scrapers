import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BuiltSpider(CrawlSpider):
    name = 'built'
    allowed_domains = ['www.dollardays.com']
    start_urls = ['https://www.dollardays.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="critically-warp"]/div[@class="container-fluid"]/div[@class="row"]//a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="product_titel"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='(//a[@title="Next Page"])[2]'), follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('normalize-space(//h2/text())').get()
        item_id = response.xpath('//li[@class="itemid"]/text()').get()
        unit_price = response.xpath('//span[@class="caseprice"]/text()').get()
        case_price = response.xpath('//h3/text()').get()
        tire_price = response.xpath('//div[@class="divTableCell PcPrice"]/span/text()').get()
        description = response.xpath('//div[@class="product-dicbar"]/ul/li')
        description_list = [desc.xpath('normalize-space(.//text())').get() for desc in description]
        description_text = ','.join(description_list)
        upc = response.xpath('normalize-space(//div[@id="ctl00_cphContent_divUPC"]/text())').get()
        brand = response.xpath('normalize-space(//div[@class="color_dic"]/text()[1])').get()
        image = response.xpath('//div[@class="owl-carousel"]/img[1]/@data-big-img').get()

        yield{
            'title':title,
            'item_id':item_id,
            'unit_price':unit_price,
            'case_price':case_price,
            'tire_price':tire_price,
            "description":description_text,
            'upc':upc,
            'brand':brand,
            'image':image,
            'url':response.url

        }

