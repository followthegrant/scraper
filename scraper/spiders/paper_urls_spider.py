import csv
import scrapy


class PaperUrlSpider(scrapy.Spider):
    name = 'paper_urls'

    def start_requests(self):
        yield scrapy.Request('https://www.nature.com/aps/articles')
        with open(self.file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield scrapy.Request('%s/articles' % row['url'])

    def parse(self, response):
        self.logger.info('Open: %s' % response.url)
        xpath = "/html/body[@class='home-page']/div[@id='content']/div[@class='container cleared container-type-article-list']/div[@class='content mb30 mq1200-padded position-relative']/div[@class='background-white pb20']/div[@class='pa20 pt30 pb0 cleared hide-overflow']/div[@class=' grid grid-8 mq875-grid-12']/div/ul[@class='ma0 mb-negative-2 clean-list grid-auto-fill']/li[@class='border-gray-medium border-bottom-1 pb20']/article/div[@class='cleared']/h3[@class='mb10 extra-tight-line-height']/a"
        next_page_xpath = "/html/body[@class='home-page']/div[@id='content']/div[@class='container cleared container-type-pagination']/div[@class='content mb20 mq1200-padded']/nav/ol[@class='clean-list pagination pagination-size-5 ma0 grid grid-12 clear']/li[@data-page='next']/a/@href"
        for item in response.xpath(xpath):
            yield {
                'title': item.xpath('text()').get().strip().replace('\n', ' '),
                'url': item.xpath('@href').get()
            }

        next_page = response.xpath(next_page_xpath).get()
        if next_page is not None:
            yield response.follow(next_page, dont_filter=True)
