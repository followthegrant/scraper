# scraper

Currently implemented: From a publisher page (like https://nature.com) scrape
list of journals, for every journal, scrape list of articles (papers) and
save the html from the individual papers to disk.

The meta information about the publishers is stored in `meta/publishers.yaml`

The scraping pipeline is build with the [scrapy](https://scrapy.org/) framework.

## usage

There are currently 3 simple spiders:
- journal index spider
- paper url spider
- paper download spider

### 1. get list of journal indexes

Scrape all publishers specified in the yaml file in the `publishers` argument
(`-a`) and save the list of journals to `./data/journals.csv`:

    scrapy crawl journal_indexes -a publishers=./meta/publishers.yaml -o ./data/journals.csv

### 2. get list of paper urls

Scrape based on the journal urls from step 1 all paper urls and save them to
`./data/papers.csv`:

    scrapy crawl paper_urls -a publishers=./meta/publishers.yaml -a journals=./data/journals.csv -o ./data/papers.csv

### 3. download papers

Once you have a list of all the papers you want to download (created in step 1
& 2), download them with this command:

    scrapy crawl papers -a papers=./data/papers.csv -a save_to=./data/papers/ -o ./data/papers/index.csv

## installation

- check out repo
- use python 3
- install `scrapy` and other dependencies (virtual environment recommended):

`pip install -r requirements.txt`
