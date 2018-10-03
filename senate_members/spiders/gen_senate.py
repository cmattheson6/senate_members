# -*- coding: utf-8 -*-
import scrapy


class GenSenateSpider(scrapy.Spider):
    name = 'gen_senate'
    
    # sends a request to the senate page to pull date
    def start_requests(self):
        start_url = 'http://www.senate.gov/general/contact_information/senators_cfm.xml'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        yield scrapy.Request(url = start_url, callback = self.parse, headers = headers)
            
    # pulls the needed data out of the senate page
    def parse(self, response):
        if response.status == 403:
            yield scrapy.Request(url = start_url, callback = self.parse, headers = headers)
        else:
            print(response.status)
            pass;
#         print(response.body)
        # get each individual member and parse out information
        for i in response.xpath("./member"):
            first_name = i.xpath("./first_name/text()").extract_first()
            last_name = i.xpath("./last_name/text()").extract_first()
            party = i.xpath("./party/text()").extract_first()
            state = i.xpath("./state/text()").extract_first()
            
            # build a dictionary for each member
            pol_dict = {
                'first_name': first_name,
                'last_name': last_name,
                'party': party,
                'state': state
                }
            
            
            # then send it to the pipeline
            yield pol_dict;
