# -*- coding: utf-8 -*-
import scrapy


class GenSenateSpider(scrapy.Spider):
    name = 'gen_senate'
    allowed_domains = ['http://www.senate.gov/general/contact_information/senators_cfm.xml']
    start_urls = ['http://www.senate.gov/general/contact_information/senators_cfm.xml']
    
    # sends a request to the senate page to pull date
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)
            
    # pulls the needed data out of the senate page
    def parse(self, response):
        # get each individual member and parse out information
        for i in response.xpath("./member"):
            first_name = response.xpath("./first_name").extract_first()
            last_name = response.xpath("./last_name/text()").extract_first()
            party = response.xpath("./party/text()").extract_first()
            state = response.xpath("./state/text()").extract_first()
            
            # build a dictionary for each member
            pol_dict = {
                'first_name': first_name,
                'last_name': last_name,
                'party': party,
                'state': state
                }
            
            # then send it to the pipeline
            yield pol_dict;
