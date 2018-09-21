# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import necessary modules
import datetime
from datetime import date
import time
from google.cloud import pubsub
from google.oauth2 import service_account
import subprocess
import scrapy
import scrapy.crawler
from scrapy.utils.project import get_project_settings
import json
import os
import tempfile
import google.auth

class SenateMembersPipeline(object):
    def process_item(self, item, spider):
        cred_dict = {
            "auth_provider_x509_cert_url": spider.settings.get('auth_provider_x509_cert_url'),
            "auth_uri": spider.settings.get('auth_uri'),
            "client_email": spider.settings.get('client_email'),
            "client_id": spider.settings.get('client_id'),
            "client_x509_cert_url": spider.settings.get('client_x509_cert_url'),
            "private_key": spider.settings.get('private_key'),
            "private_key_id": spider.settings.get('private_key_id'),
            "project_id": spider.settings.get('project_id'),
            "token_uri": spider.settings.get('token_uri'),
            "type": spider.settings.get('account_type')
            }
        print(cred_dict)
        cred_json = json.dumps(cred_dict)
               
        # Create a temporary file here
        fd, path = tempfile.mkstemp(suffix='.json')
        print(path)

        # Then use a 'with open' statement as shown in the stackoverflow comments
        with os.fdopen(fd, 'w') as tmp:
            json.dump(cred_dict, tmp)
            tmp.close()

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        
        # quick check to make sure everything is good
        print(os.path.exists(path))
        credentials, project_id = google.auth.default()
        print(project_id)
        print(credentials)
         
        print(os.path.exists(path))
        publisher = pubsub.PublisherClient()
        
        topic = 'projects/{project_id}/topics/{topic}'.format(
             project_id='politics-data-tracker-1',
             topic='') ###TO DO: FILL THIS IN IF/WHEN I MAKE A NEW TOPIC
        publisher.publish(topic, b'This is a representative in the Senate.', 
                          first_name = item['first_name'],
                          last_name = item['last_name'],
                          party = item['party'],
                          state = item['state'])
        os.remove(path)
