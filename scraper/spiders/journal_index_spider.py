import scrapy

from datetime import datetime

from util import slugify, get_publishers


class JournalIndexSpider(scrapy.Spider):
    name = 'journal_indexes'

    def start_requests(self):
        for publisher in get_publishers(self.publishers):
            if not publisher.get('ignore_index'):
                yield scrapy.Request(publisher['index_url'], meta=publisher, dont_filter=True)

    def parse(self, response):
        self.logger.info('Index: %s' % response.url)
        xpath = response.meta['journal_items_xpath']
        for item in response.xpath(xpath):
            journal_name = item.xpath('text()').get()
            yield {
                'ts': datetime.now().isoformat(),
                'publisher_name': response.meta['name'],
                'publisher_slug': response.meta['slug'],
                'publisher_url': response.meta['url'],
                'journal_name': journal_name,
                'journal_slug': slugify(journal_name),
                'journal_url': item.xpath('@href').get()
            }
