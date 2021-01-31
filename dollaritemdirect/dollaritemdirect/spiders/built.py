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
        # pagination need to be added
        )

    def parse_details(self, response):
        title = response.xpath('//div[@class="center_block_1"]/h2/span/text()').get()
        price_list = response.xpath('//span[@class="prod-detail-cost-value"]//text()').getall()
        prices = ','.join(price_list)
        description_list = response.xpath('//div[@class="prod-detail-desc"]//li')        
        if len(description_list) == 0:
            description_list = response.xpath('//div[@class="prod-detail-desc"]')
        normalized_description_list = [desc.xpath('normalize-space(.//text())').get() for desc in description_list]      

        descriptions = ', '.join(normalized_description_list)
        descriptions = descriptions.strip()
        yield{
            'title':title,
            'price':prices,
            'descriptions':descriptions,
            'url':response.url,
        }
        
