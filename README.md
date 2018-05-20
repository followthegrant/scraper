# scraper

Example for now: https://nature.com

1. get list of journal indexes

`scrapy crawl journal_indexes -o nature_journals.csv`

2. get list of paper urls (from step 1)

`scrapy crawl paper_urls -a file=nature_journals.csv -o nature_papers.csv`

## installation

- check out repo
- create python3 virtualenv
- install `scrapy` via:

`pip install -r requirements.txt`
