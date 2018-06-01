import csv
import scrapy

from datetime import datetime

from util import slugify, get_publishers


class PaperUrlSpider(scrapy.Spider):
    name = 'paper_urls'

    def start_requests(self):
        publishers = {p['slug']: p for p in get_publishers(self.publishers)}
        with open(self.journals) as f:
            reader = csv.DictReader(f)
            for journal in reader:
                publisher = publishers[journal['publisher_slug']]
                journal['publisher_meta'] = publisher
                url = journal['journal_url']
                if 'paper_index_url_eval' in publisher:
                    get_url = eval(publisher['paper_index_url_eval'])
                    url = get_url(journal['journal_url'])
                yield scrapy.Request(url, meta=journal)

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)
        xpath = response.meta['publisher_meta']['paper_items_xpath']
        next_page_xpath = response.meta['publisher_meta']['paper_index_nextpage_xpath']
        publisher_name = response.meta['publisher_meta']['name']
        publisher_slug = slugify(publisher_name)
        for item in response.xpath(xpath):
            yield {
                'ts': datetime.now().isoformat(),
                'publisher_name': publisher_name,
                'publisher_slug': publisher_slug,
                'journal_name': response.meta['journal_name'],
                'journal_slug': response.meta['journal_slug'],
                'title': item.xpath('text()').get().strip().replace('\n', ' '),
                'base_url': response.meta['download_slot'],
                'url': item.xpath('@href').get()
            }

        next_page = response.xpath(next_page_xpath).get()
        if next_page is not None:
            yield response.follow(next_page, dont_filter=True, meta=response.meta)
