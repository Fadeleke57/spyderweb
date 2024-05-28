from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://time.com/search/?q=apple",
    ]

    def parse(self, response):
        page = 3
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)