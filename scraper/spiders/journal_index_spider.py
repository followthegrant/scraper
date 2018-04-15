import scrapy


class JournalIndexSpider(scrapy.Spider):
    name = 'journal_indexes'
    start_urls = [
        'https://www.nature.com/siteindex/index.html',
    ]

    def parse(self, response):
        self.logger.info('Index: %s' % response.url)
        xpath = "/html/body[@class='article-page']/div[@id='content']/div[@id='journals-az']/div[@id='back-to-top']/div/div[@class='grid grid-8 mb20 mq640-grid-12 mq640-last']/div/ul[@class='ma0 cleared clean-list grid grid-10']/li/a[@class='block pt10 pb10 equalize-line-height']"
        for item in response.xpath(xpath):
            yield {
                'journal_name': item.xpath('text()').get(),
                'url': item.xpath('@href').get()
            }
