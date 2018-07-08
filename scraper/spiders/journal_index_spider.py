import scrapy

from datetime import datetime

from util import slugify, get_publishers, get_absolute_url


class JournalIndexSpider(scrapy.Spider):
    name = 'journal_indexes'

    def start_requests(self):
        for publisher in get_publishers(self.publishers):
            if (self.publisher and publisher['slug'] == self.publisher)\
               or not self.publisher\
               and not publisher.get('ignore_index'):
                yield scrapy.Request(publisher['index_url'], meta=publisher, dont_filter=True)

    def parse(self, response):
        self.logger.info('Index: %s' % response.url)
        xpath = response.meta['journal_items_xpath']
        name_xpath = 'text()'
        url_xpath = '@href'
        if isinstance(xpath, dict):
            name_xpath = xpath['name']
            url_xpath = xpath['url']
            xpath = xpath['item']
        for item in response.xpath(xpath):
            journal_name = item.xpath(name_xpath).get()
            journal_url = get_absolute_url(response.url, item.xpath(url_xpath).get())
            if journal_name and journal_url:
                yield {
                    'ts': datetime.now().isoformat(),
                    'publisher_name': response.meta['name'],
                    'publisher_slug': response.meta['slug'],
                    'publisher_url': response.meta['url'],
                    'journal_name': journal_name,
                    'journal_slug': slugify(journal_name),
                    'journal_url': journal_url
                }
