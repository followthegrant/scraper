"""
obtain paper index urls from an archive page like this:
    https://www.thelancet.com/journals/lanplh/issues
"""

import requests
from scrapy.http import TextResponse
from scrapy.utils.project import get_project_settings


header = {
    'User-Agent': get_project_settings()['USER_AGENT']
}


def extract(url):
    res = requests.get(url, headers=header)
    response = TextResponse(url, body=res.text.encode())
    for url in response.xpath("//div[@class='loi ']//div[@id='issueName']/a[@class='issueLinkCon']/@href"):
        yield response.urljoin(url.get())
