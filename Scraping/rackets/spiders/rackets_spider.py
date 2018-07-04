# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:47:38 2018

@author: ratanond
"""

import scrapy
from rackets.items import RacketsItem

class RacketsSpider(scrapy.Spider):
    name = "rackets"
    allowed_domains = ["tennisexpress.com"]
    
    #start_urls = ["https://www.tennisexpress.com/wilson-tennis-racquets"]
    #start_urls = ["https://www.tennisexpress.com/babolat-tennis-racquets"]
    #start_urls = ["https://www.tennisexpress.com/head-tennis-racquets"]
    start_urls = ["https://www.tennisexpress.com/yonex-tennis-racquets"]
    
    def parse(self, response):
        for racket_url in response.xpath('//section[@class="productList"]//a/@href').extract():
            yield scrapy.Request(racket_url,callback = self.parse_racket)
            
    def parse_racket(self, response):
        item = RacketsItem()
        item['Price'] = response.xpath('//*[@id="price"]/text()').extract()
        item['Sale_Price'] = response.xpath('//*[@id="salePrice"]/text()').extract()
        item['Racket_Name'] = response.xpath('//aside[@id="prodNamBrCont"]/p/text()').extract()
#        item['Head_Size'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[1]/td[2]/text()').extract()
#        item['Length'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[2]/td[2]/text()').extract()
#        item['Weight'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[3]/td[2]/text()').extract()
#        item['Tension'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[4]/td[2]/text()').extract()
#        item['Balance'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[5]/td[2]/text()').extract() 
#        item['Beam_Width'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[6]/td[2]/text()').extract() 
#        item['Composition'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[7]/td[2]/text()').extract() 
#        item['Flex'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[8]/td[2]/text()').extract()
#        item['Grip_Type'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[9]/td[2]/text()').extract() 
#        item['Power_Level'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[10]/td[2]/text()').extract() 
#        item['String_Pattern'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[11]/td[2]/text()').extract() 
#        item['Swing_speed'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[12]/td[2]/text()').extract() 
#        item['Swingweight'] = response.xpath('//div[@id="tabContainer"]//*[@id="RacquetSpecsTable"]//tr[13]/td[2]/text()').extract() 
    
        yield item
        
        #https://stackoverflow.com/questions/30218818/scrapy-returning-a-null-output-when-extracting-an-element-from-a-table-using-xpa