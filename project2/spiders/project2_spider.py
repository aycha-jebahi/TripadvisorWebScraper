import scrapy
from project2.items import Project2Item
from scrapy import Spider
from scrapy.selector import Selector
import re
 
class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"
    allowed_domains = ["www.tripadvisor.com"]

    def start_requests(self):

        urls = [
         "https://www.tripadvisor.com/Hotel_Review-g297948-d302589-Reviews-El_Mouradi_Djerba_Menzel-Midoun_Djerba_Island_Medenine_Governorate.html"]
 

      
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Fonction parse_review() pour accéder à une review et extraire les données
        for href in response.xpath('//div[@class="location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)
        
        next_page = response.xpath('//a[@class="ui_button nav next primary "]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

   

    def parse_review(self, response):
       # Fonction parse() pour parcourir tous les reviews 
       item = Project2Item()
       item['hotel'] =  response.xpath('//div[@class="altHeadInline"]/a/text()').extract()[0]
       item['url'] =  response.xpath('//a[@class="ui_header h2"]//@href').extract()[0]
       item['name'] =  response.xpath('//div[@class="info_text"]/div/text()').extract()[0]
       item['title'] = response.xpath('//h1[@class="title"]/text()').extract()[0] 

       item['country'] =  response.xpath('//div[@class="info_text"]/div[@class="userLoc"]/strong/text()').extract()[0]

       item['content'] = response.xpath('//span[@class="fullText hidden"]/text()').extract()[0]
       item['dateOfstay'] =  response.xpath('//div[@class="prw_rup prw_reviews_stay_date_hsx"]/text()').extract()[0]

       yield item

    




