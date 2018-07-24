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
        
        codigo = response.xpath('//span[contains(text(), "Código do Imovelweb")]/text()').extract_first()
        if codigo:
            item['code'] = re.sub("\D", "", codigo)
        
        item['url'] = response.url
        item['lat'] = response.xpath('//input[@type="hidden" and @name="lat"]/@value').extract_first()
        item['lng'] = response.xpath('//input[@type="hidden" and @name="lng"]/@value').extract_first()
        
        price = response.xpath('//p[contains(@class, "precios")]/strong/text()').extract_first()
        if price:
            item['price'] = re.sub("\D", "", price)
        
        common_price = response.xpath('//*[contains(text(), "Condomínio:")]/text()').extract_first()
        if common_price:
            item['common_price'] = re.sub("\D", "", common_price)
        
        area_total = response.xpath('//*[contains(text(), "Área total:")]/text()').extract_first()
        if area_total:
            item['area_total'] = re.sub("\D", "", area_total)

        area_util = response.xpath('//*[contains(text(), "Área útil:")]/text()').extract_first()
        if area_util:
            item['area_util'] = re.sub("\D", "", area_util)

        banheiros = response.xpath('//*[contains(text(), "Banheiros:")]/text()').extract_first()
        if banheiros:
            item['banheiros'] = re.sub("\D", "", banheiros)

        suites = response.xpath('//*[contains(text(), "Suites:")]/text()').extract_first()
        if suites:
            item['suites'] = re.sub("\D", "", suites)

        
        idade = response.xpath('//*[contains(text(), "Idade do imóvel:")]/text()').extract_first()
        if idade:
            item['idade'] = re.sub("\D", "", idade)

        vagas = response.xpath('//*[contains(text(), "Vagas:")]/text()').extract_first()
        if vagas:
            item['vagas'] = re.sub("\D", "", vagas)

        yield item

        # client = MongoClient("mongodb://admin:macacoveio10@ds117148.mlab.com:17148/imob", 17148)
        client = MongoClient("localhost:27017")
        
        db = client["imob"]
        posts = db.ad
        result = posts.insert_one(dict(item))
        print('Posted: {0}'.format(result.inserted_id))
