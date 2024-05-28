import scrapy
from scrapy_selenium import SeleniumRequest

class TimeSpider(scrapy.Spider):
    name = "time"

    def start_requests(self):
        search_term = getattr(self, "search_term", None)
        start_urls = [f'https://time.com/search/?q={search_term}']
        for url in start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # save the rendered HTML response to a file for debugging purposes

        
        articles = response.css('article.partial.tile.media.image-top.search-result')

        for article in articles:
            header = article.css('div.headline a::text').get()
            article_link = article.css('div.headline a::attr(href)').get()
            yield SeleniumRequest(url=article_link, callback=self.parse_article, meta={'header': header, 'link': article_link})
            # extract next page link
            #next_page = response.css('a.arrow.next::attr(href)').get()
            #if next_page:
               #next_page_url = response.urljoin(next_page)
               #yield SeleniumRequest(url=next_page_url, callback=self.parse)
            
            #yield {
            #    'header': header,
            #    'link': article_link,
            #    'next_page' : next_page
            #}

    def parse_article(self, response):
        header = response.meta['header']
        link = response.meta['link']

        with open('rendered_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)  

        dates = response.css('time::text').getall()
        date = " | ".join(dates)
        if date == "":
            date = response.css('span.entry-date::text').get()
        author =  response.css('a[href*="/author/"]::text').get()
        # extract text from <p> tags including text from nested <a> tags
        paragraphs = response.css('p').xpath('string(.)').getall()
        full_text = ' '.join(paragraphs)

        # extract nested links within <p> tags
        nested_links = response.css('p a::attr(href)').getall()
        nested_links = [response.urljoin(url) for url in nested_links]

        yield {
            'header': header,
            'author': author,
            'update/publish': date,
            'link': link,
            'date' : date,
            'text': full_text,
            'nested_links': nested_links,
        }
