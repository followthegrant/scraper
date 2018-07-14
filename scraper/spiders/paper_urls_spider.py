# import importlib
import csv
import scrapy

from datetime import datetime

from scraper import extractors  # FIXME python import foo
from util import get_publisher


class PaperUrlSpider(scrapy.Spider):
    name = 'paper_urls'

    def start_requests(self):
        publisher = get_publisher(self.publisher)
        if hasattr(self, 'journals'):
            with open(self.journals) as f:
                journals = list(csv.DictReader(f))
        else:
            journals = [{
                'publisher_slug': p['slug'],
                'publisher_name': p['name'],
                'journal_name': p['name'],
                'journal_slug': p['slug'],
                'journal_url': p['paper_index_url']
            } for p in [publisher] if p.get('paper_index_url')]

        for journal in journals:
            journal['publisher_meta'] = publisher
            url = journal['journal_url']
            if 'paper_index_url_eval' in publisher:
                get_url = eval(publisher['paper_index_url_eval'])
                url = get_url(journal['journal_url'])
            url_extractor = publisher.get('paper_index_urls_extractor')
            if url_extractor:
                # FIXME python import foo
                # extractor = importlib.import_module('scraper.extractors', package=url_extractor)
                extractor = getattr(extractors, url_extractor)
                for url in extractor.extract(url):
                    yield scrapy.Request(url, meta=journal, dont_filter=True)
            else:
                    yield scrapy.Request(url, meta=journal, dont_filter=True)

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)
        xpath = response.meta['publisher_meta']['paper_items_xpath']
        name_xpath = 'text()'
        url_xpath = '@href'
        if isinstance(xpath, dict):
            name_xpath = xpath['name']
            url_xpath = xpath['url']
            xpath = xpath['item']
        next_page_xpath = response.meta['publisher_meta'].get('paper_index_nextpage_xpath')
        for item in response.xpath(xpath):
            title = item.xpath(name_xpath).get()
            url = response.urljoin(item.xpath(url_xpath).get())
            if title and url:
                yield {
                    'ts': datetime.now().isoformat(),
                    'publisher_name': response.meta['publisher_name'],
                    'publisher_slug': response.meta['publisher_slug'],
                    'journal_name': response.meta['journal_name'],
                    'journal_slug': response.meta['journal_slug'],
                    'title': title.strip().replace('\n', ' '),
                    'url': url
                }

        if next_page_xpath:
            next_page = response.xpath(next_page_xpath).get()
            if next_page is not None:
                yield response.follow(next_page, dont_filter=True, meta=response.meta)
