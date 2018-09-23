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
        # Pull in the spider service account info for authorization
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

        # Run the authorization and receive a set of credentials back from Google Cloud
        credentials = service_account.Credentials.from_service_account_info(cred_dict)
        print(credentials)
        print("I haven't set up the client yet, but I built the credentials!")
        
        # Set up the Google client and explicitly use the credentials you just received
        publisher = pubsub.PublisherClient(credentials = credentials)
        print(publisher)
        print("The client was set up!")
        
        # Publish the item to the designated Pub/Sub topic
        topic = 'projects/{project_id}/topics/{topic}'.format(
             project_id='politics-data-tracker-1',
             topic='house_pols')
        project_id = 'politics-data-tracker-1'
        topic_name = 'senate_pols'
        topic_path = publisher.topic_path(project_id, topic_name)
        data = u'This is a representative in the Senate.'
        data = data.encode('utf-8')
        print("The topic was built!")
        publisher.publish(topic_path, data=data,
                          first_name = item['first_name'],
                          last_name = item['last_name'],
                          party = item['party'],
                          state = item['state'])
        print("We published! WOOOO!")
