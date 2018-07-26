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
    start_urls = ['https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-1-quarto.html',
                  'https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-2-quartos.html',
                  'https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-3-quartos.html',
                  'https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-4-quartos.html',
                  'https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-5-quartos.html',
                  'https://www.imovelweb.com.br/apartamentos-padrao-venda-vila-mariana-sao-paulo-mais-de-6-quartos.html'
                ]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination-action-next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print(response.url)
            
        item_links = response.css('.dl-aviso-a::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(response.urljoin(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        
        item = ImobItem()
        code_number = 0
        code = response.xpath('//span[contains(text(), "Código do Imovelweb")]/text()').extract_first()
        price = response.xpath('//p[contains(@class, "precios")]/strong/text()').extract_first()
        item['lat'] = response.xpath('//input[@type="hidden" and @name="lat"]/@value').extract_first()
        item['lng'] = response.xpath('//input[@type="hidden" and @name="lng"]/@value').extract_first()
        
        if code and price and item['lat'] or item['lng']:
            item['url'] = response.url
            code_number = re.sub("\D", "", code)
            item['code'] = code_number
            item['price'] = re.sub("\D", "", price)
            common_price = response.xpath('//*[contains(text(), "Condomínio:")]/text()').extract_first()
            if common_price:
                item['common_price'] = re.sub("\D", "", common_price)
            
            total_area = response.xpath('//*[contains(text(), "Área total:")]/text()').extract_first()
            if total_area:
                item['total_area'] = re.sub("\D", "", total_area)

            util_area = response.xpath('//*[contains(text(), "Área útil:")]/text()').extract_first()
            if util_area:
                item['util_area'] = re.sub("\D", "", util_area)

            bathrooms = response.xpath('//*[contains(text(), "bathrooms:")]/text()').extract_first()
            if bathrooms:
                item['bathrooms'] = re.sub("\D", "", bathrooms)

            suites = response.xpath('//*[contains(text(), "Suites:")]/text()').extract_first()
            if suites:
                item['suites'] = re.sub("\D", "", suites)

            age = response.xpath('//*[contains(text(), "age do imóvel:")]/text()').extract_first()
            if age:
                item['age'] = re.sub("\D", "", age)

            parking = response.xpath('//*[contains(text(), "parking:")]/text()').extract_first()
            if parking:
                item['parking'] = re .sub("\D", "", parking)

            yield item

            # client = MongoClient("mongodb://admin:macacoveio10@ds117148.mlab.com:17148/imob", 17148)
            client = MongoClient("localhost:27017")
            db = client["imob"]
            posts = db.ad

            result = ""
            if posts.find_one({"code": code_number}):
                posts.update_one({"code": code_number},{"$set": {"price": price}})
                print('Updated:', code_number)
            else:
                result = posts.insert_one(dict(item))
                print('Posted:', format(result.inserted_id))
        else:
            pass