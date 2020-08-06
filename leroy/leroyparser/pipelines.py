# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
import os.path
from urllib.parse import urlparse
from pymongo import MongoClient
import scrapy
# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        item['specs'] = dict(zip(item['specs_params'], item['specs_values']))
        item.pop('specs_params')
        item.pop('specs_values')

        collection.insert_one(item)
        return item


class LeroyPicPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):

        return f'files/{request.meta.get("filename", "")}/{os.path.basename(urlparse(request.url).path)}'

    def get_media_requests(self, item, info):
        meta = {'filename': item['title']}
        if item['pictures']:
            for img in item['pictures']:
                try:
                    yield scrapy.Request(img, meta=meta)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['pictures'] = [itm[1] for itm in results if itm[0]]
        return item
