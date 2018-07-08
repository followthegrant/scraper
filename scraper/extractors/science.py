"""
obtain paper urls from an archive page like this:
    http://science.sciencemag.org/content/by/year
"""

import requests
# import scrapy
# from scrapy import signals
# from scrapy.crawler import Crawler
from scrapy.http import TextResponse
from scrapy.utils.project import get_project_settings

from util import get_absolute_url


header = {
    'User-Agent': get_project_settings()['USER_AGENT']
}

# class SciencePaperUrlSpider(scrapy.Spider):
#     name = 'science_index'

#     def __init__(self, *args, **kwargs):
#         self.start_urls = kwargs.pop('urls')
#         super().__init__(*args, **kwargs)

#     def parse(self, response):
#         self.logger.info('Open: %s' % response.url)
#         for item in response.xpath("//ul[@class='issue-month-detail']/li/div/div/a/@href"):
#             yield {'url': response.urljoin(response.url, item.get())}


def _get_years_urls(response):
    # 2010s
    for url in response.xpath("//ul[@class='issue-browser years 2010 highwire-list active']/li/a/@href"):
        yield get_absolute_url(response.url, url.get())
    # 2000s
    for url in response.xpath("//ul[@class='issue-browser years 2000 highwire-list']/li/a/@href"):
        yield get_absolute_url(response.url, url.get())


# def get_item(item, response, spider):
#     import ipdb; ipdb.set_trace()


def extract(url):
    # urls = list(_get_years_urls(response))
    # crawler = Crawler(SciencePaperUrlSpider, get_project_settings())
    # crawler.signals.connect(get_item, signal=signals.item_scraped)
    # crawler.crawl(urls=urls)
    res = requests.get(url, headers=header)
    resp = TextResponse(url, body=res.text.encode())
    for url in _get_years_urls(resp):
        res = requests.get(url, headers=header)
        response = TextResponse(url, body=res.text.encode())
        for url in response.xpath("//ul[@class='issue-month-detail']/li/div/div/a/@href"):
            yield response.urljoin(url.get())
