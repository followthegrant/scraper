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
                url = journal['journal_url']
                import ipdb; ipdb.set_trace()
                if 'paper_index_url_eval' in publisher:
                    get_url = eval(publisher['paper_index_url_eval'])
                    url = get_url(journal['journal_url'])
                yield scrapy.Request(url, meta=journal)

    def parse(self, response):
        import ipdb; ipdb.set_trace()
        self.logger.info('Open: %s' % response.url)
        xpath = response.meta['paper_items_xpath']
        next_page_xpath = response.meta['paper_index_nextpage_xpath']
        for item in response.xpath(xpath):
            yield {
                'ts': datetime.now().isoformat(),
                'journal_name': response.meta['journal_name'],
                'journal_slug': response.meta['journal_slug'],
                'title': item.xpath('text()').get().strip().replace('\n', ' '),
                'base_url': response.meta['download_slot'],
                'url': item.xpath('@href').get()
            }

        next_page = response.xpath(next_page_xpath).get()
        if next_page is not None:
            yield response.follow(next_page, dont_filter=True)
