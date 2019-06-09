import csv
import scrapy
import os
import sys
from datetime import datetime
from uuid import uuid4

from util import slugify


class PaperSpider(scrapy.Spider):
    name = 'papers'

    def start_requests(self):
        try:
            with open(sys.argv[-1]) as f:
                reader = csv.DictReader(f)
                urls = [r['url'] for r in reader]
        except FileNotFoundError:
            urls = []

        with open(self.papers) as f:
            reader = csv.DictReader(f)
            papers = [r for r in reader]

        # make unique
        papers = list({p['url']: p for p in papers}.values())

        for paper in papers:
            if paper['url'] not in urls:
                yield scrapy.Request(paper['url'], meta=paper)

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)

        if response.status == 200:
            fname = os.path.join(
                self.save_to,
                response.meta['journal_slug'],
                '%s--%s.html' % (slugify(response.meta['title'][:50]), str(uuid4()))
            )
            os.makedirs(os.path.split(fname)[0], exist_ok=True)
            with open(fname, 'w') as f:
                f.write(response.text)
                self.logger.info('Saved to: %s' % fname)

        yield {
            'url': response.url,
            'status': response.status,
            'ts': datetime.now().isoformat(),
            'path': fname
        }
