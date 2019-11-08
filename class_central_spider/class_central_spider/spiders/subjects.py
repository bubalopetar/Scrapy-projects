# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request 

class SubjectsSpider(Spider):
    name = 'subjects'
    #allowed_domains = ['class-central.com']
    start_urls = ['http://class-central.com/subjects']

    def __init__(self,subject=None):
        self.subject=subject

    def parse(self, response):

        # If we send argument with " scrapy crawl subjects -a subject="Programming" ",  then go to category.
        if self.subject:
           subject_url=response.xpath('//a[contains(@title,"'+self.subject+'")]//@href').get()
           yield Request(response.urljoin(subject_url),self.parse_subjects)
        else:
            self.logger.info("Scraping all subjects")
            subjects=response.xpath('//a[@class="col align-middle padding-right-xsmall"]//@href').getall()
            
            for subject in subjects:
                yield Request(response.urljoin(subject),callback=self.parse_subjects)
                

    def parse_subjects(self,response):
         subject_name=response.xpath("//h1[@class='head-1']//text()").get()
         courses=response.xpath('//a[@class="color-charcoal block course-name"]')

         for course in courses:
             course_url=course.xpath('@href').get()
             course_name=course.xpath('.//span//text()').get()
             absoulte_url=response.urljoin(course_url)
             yield{

                "course_url":course_url,
                "course_name":course_name,
                "absoulte_url":absoulte_url

             }
                
         next_page=response.xpath("//link[@rel='next']//@href").get()
         absoulte_next=response.urljoin(next_page)

         yield Request(absoulte_next,callback=self.parse_subjects)