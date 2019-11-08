# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class RadioSpider(scrapy.Spider):
    name = 'radio'
    #allowed_domains = ['https://radioimotski.hr/']
    start_urls = ['http://radioimotski.hr//']

    def parse(self, response):
        
        for article in response.xpath('//article'):
            link=article.xpath('.//a//@href').get()
            yield Request(link,callback=self.parse_article)

        next_page=response.xpath('.//a[@class="next page-numbers"]//@href').get()
        yield Request(next_page)
    
    def parse_article(self,response):

        title=response.xpath('.//h1[@class="title single-title entry-title"]//text()').get()
        link=response.url
        article_text=response.xpath('.//div[@class="pf-content"]//text()').getall()
        article_text=''.join(article_text)
        tags=response.xpath('//div[@class="tags"]//text()').getall()
        author=response.xpath('.//span[@class="theauthor"]//a//text()').get()
        date=response.xpath('.//span[@class="thetime date updated"]//text()').get()
        category=response.xpath('.//span[@class="thecategory"]//a//text()').getall()
        views=response.xpath('.//div[@class="views"]//text()')[1].get().strip()
        likes=response.xpath('.//span[@class="sl-count"]//text()').get()
        
        data={
            'Title':title,
            'Link':link,
            'Article':article_text,
            'Tags':tags,
            'Author':author,
            'Date':date,
            'Category':category,
            'Views':views,
            'Likes':likes
        }
        yield data
