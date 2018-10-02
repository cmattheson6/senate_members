# -*- coding: utf-8 -*-
import scrapy


class GenSenateSpider(scrapy.Spider):
    name = 'gen_senate'
    
    # sends a request to the senate page to pull date
    def start_requests(self):
        start_url = 'http://www.senate.gov/general/contact_information/senators_cfm.xml'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        yield scrapy.Request(url = start_url, callback = self.parse, headers = headers)
            
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
