import csv
import scrapy
import os
from datetime import datetime
from slugify import slugify


class PaperSpider(scrapy.Spider):
    name = 'papers'

    def start_requests(self):
        with open(self.file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield scrapy.Request(''.join((self.base_url, row['url'])))

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)

        if response.status == 200:
            fname = os.path.join(self.save_to, '%s.html' % slugify(response.url[len(self.base_url):]))
            with open(fname, 'w') as f:
                f.write(response.text)
                self.logger.info('Saved to: %s' % fname)

        yield {
            'url': response.url,
            'status': response.status,
            'ts': datetime.now().isoformat(),
            'path': os.path.realpath(fname)
        }
