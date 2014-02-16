# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy import log

from baidubuzz.utils import *


class BaidubuzzPipeline(object):
    def process_item(self, item, spider):

        return item

class ValidatePipeline(object):
    def process_item(self, item, spider):
        if item['rank'] and item['keyword'] and item['searchIndex']:
            return item
        else:
            raise DropItem("Missing field in %s" % item)

class CouchDBPipeline(object):
    def __init__(self):
        import couchdb
        server = couchdb.Server(settings['COUCHDB_URL'])
        try:
    		self.db = server.create(settings['COUCHDB_DB'])
    	except couchdb.http.PreconditionFailed, e:
        	self.db = server[settings['COUCHDB_DB']]

    def process_item(self, item, spider):
    	doc_id, doc_rev = self.db.save({'rank': item['rank'], 'keyword': item['keyword'],
    		'searchIndex': item['searchIndex'], 'date': covertDatetime(item['date'])})
        log.msg("Item wrote to CouchDB database %s, doc_id %s" %
                    (settings['COUCHDB_DB'], doc_id), 
                    level=log.DEBUG, spider=spider)
        return item
