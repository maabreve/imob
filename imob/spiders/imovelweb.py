# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imob.items import ImobItem
import re  
from pymongo import MongoClient
from imob.models.ad import Post

class ImovelwebSpider(CrawlSpider):
    name = "imovelweb"
    allowed_domains = ['imovelweb.com.br']
    start_urls = ['https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-1-quarto.html',
                'https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-2-quartos.html',
                'https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-3-quartos.html',
                'https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-4-quartos.html',
                'https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-5-quartos.html',
                'https://www.imovelweb.com.br/apartamentos-padrao-vila-mariana-sao-paulo-mais-de-6-quartos.html'
                ]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination-action-next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('----------->', response.url)
            
        item_links = response.css('.dl-aviso-a::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        # title = response.css('h1::text').extract()[0].strip()
        # price = response.css('.pricelabel > .xxxx-large').extract()[0]
        item = ImobItem()
        item['code'] = re.sub("\D", "", response.xpath('//span[contains(text(), "Código do Imovelweb")]/text()').extract_first())
        item['url'] = response.url
        item['lat'] = response.xpath('//input[@type="hidden" and @name="lat"]/@value').extract_first()
        item['lng'] = response.xpath('//input[@type="hidden" and @name="lng"]/@value').extract_first()
        
        # print(item)
        yield item

        client = MongoClient("mongodb://admin:macacoveio10@ds117148.mlab.com:17148/imob", 17148)
        db = client["imob"]
        posts = db.ad
        result = posts.insert_one(dict(item))
        print('Posted: {0}'.format(result.inserted_id))
