from scrapy.spider import Spider
from scrapy.selector import Selector
from baidubuzz.items import BaidubuzzItem
from datetime import *

class BaiduBuzzSpider(Spider):
    name = "baidubuzz"
    allowed_domains = ["top.baidu.com"]
    start_urls = ["http://top.baidu.com/buzz?b=2&c=12"]
  
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//table[@class="list-table"]/tr')
        items = []
        today = date.today()
        for site in sites:
            item = BaidubuzzItem()
            item['rank'] = site.xpath('td[@class="first"]/span/text()').extract()
            item['keyword'] = site.xpath('td[@class="keyword"]/a[@class="list-title"]/text()').extract()
            item['searchIndex'] = site.xpath('td[@class="last"]/span/text()').extract()
            item['date'] = today
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'
        return items
