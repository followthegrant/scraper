import csv
import scrapy
import os
from datetime import datetime

from util import slugify


class PaperSpider(scrapy.Spider):
    name = 'papers'

    def start_requests(self):
        with open(self.papers) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield scrapy.Request('https://{base_url}{url}'.format(**row), meta=row)  # FIXME http scheme

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)

        if response.status == 200:
            fname = os.path.join(self.save_to, '%s.html' % slugify(response.meta['title']))
            with open(fname, 'w') as f:
                f.write(response.text)
                self.logger.info('Saved to: %s' % fname)

        yield {
            'url': response.url,
            'status': response.status,
            'ts': datetime.now().isoformat(),
            'path': os.path.realpath(fname)
        }
