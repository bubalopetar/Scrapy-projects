# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class DealerSpider(scrapy.Spider):
    name = 'dealer'
    #allowed_domains = ['https://www.control4.com/dealer_locator/list']
    start_urls = ['https://www.control4.com/dealer_locator/list/']

    def parse(self, response):
        
        for country in response.xpath('//div[@class="row padding-top-half"]//@href').getall():
            country_url=response.urljoin(country)
            yield Request(country_url,callback=self.parse_country)
            

    def parse_country(self,response):
        
        for company in response.xpath('//div[@class="dealer-result"]//a//@href').getall():
            company_url=response.urljoin(company)
            country=response.xpath('//div[@class="container padding-top padding-bottom"]//text()').get()[10:]
            yield Request(company_url,callback=self.parse_company,meta={'country':country})
            
    
    def parse_company(self,response):
        name=response.xpath('//div[@class="container padding-top padding-bottom"]//h1//text()').get()
        #description=response.xpath('//div[@class="container padding-top padding-bottom"]//p//text()').get()
        address=response.xpath('//div[@class="col-xs-8 col-sm-6 address"]//text()').getall()
        address=' '.join(address)
        contact=response.xpath('//div[@class="col-xs-push-4 col-xs-8 col-md-push-0 col-sm-3 contact"]//text()').getall()[:-1]
        web=response.xpath('//div[@class="col-xs-push-4 col-xs-8 col-md-push-0 col-sm-3 contact"]//a//@href').get()
        web=response.urljoin(web)

        yield{
            'Country':response.meta['country'],
            'Company Name':name,
            #'Description':description,
            'Address':address,
            'Contact':contact,
            'Website':web
        }