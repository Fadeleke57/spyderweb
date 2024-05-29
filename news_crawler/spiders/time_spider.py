import scrapy
from scrapy_selenium import SeleniumRequest

class TimeSpider(scrapy.Spider):
    name = "time"

    def __init__(self, search_term=None, *args, **kwargs):
        super(TimeSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term
    
    def start_requests(self):
        search_term = self.search_term
        start_urls = [f'https://time.com/search/?q={search_term}']
        for url in start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_search_results, meta={'search_term': search_term})

    def parse_search_results(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve search results: {response.url} with status {response.status}")

        articles = response.css('article.partial.tile.media.image-top.search-result')
        search_term = self.search_term

        for article in articles:
            header = article.css('div.headline a::text').get()
            article_link = article.css('div.headline a::attr(href)').get()
            yield SeleniumRequest(url=article_link, callback=self.parse_article, meta={'header': header, 'link': article_link})  

            #next_page = response.css('a.arrow.next::attr(href)').get() # extract next page link
            #if next_page:
            #    next_page_url = response.urljoin(next_page)
            #    yield SeleniumRequest(url=next_page_url, callback=self.parse_search_results)
            for i in range(2, 4):
                next_page_url = f'https://time.com/search/?q={search_term}&page={i}'
                yield SeleniumRequest(url=next_page_url, callback=self.parse_search_results)

    def parse_article(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve article: {response.url} with status {response.status}")

        header = response.meta['header']
        link = response.meta['link']

        dates = response.css('time::text').getall()
        date = " | ".join(dates)
        if date == "":
            date = response.css('span.entry-date::text').get() #accounting for differnt Time website formats - will probably make a list of possible selectors for each attribute if i scale  
        author =  response.css('a[href*="/author/"]::text').get()
        
        paragraphs = response.css('p').xpath('string(.)').getall()
        full_text = " ".join(paragraphs)

        nested_links = response.css('p a::attr(href)').getall() # nested links are <a> tags within <p> tags
        nested_links = [response.urljoin(url) for url in nested_links]

        yield {
            'type': 'article',
            'header': header,
            'author': author,
            'update_date/publish_date': date,
            'link': link,
            'text': full_text,
            'nested_links': nested_links,
        }

"""
------------------DEBUGGING UTILITY-----------------------------------------------      

 with open('rendered_response.html', 'w', encoding='utf-8') as f:
    #f.write(response.text)  

-------------------------USEFUL----------------------------------------------------
Speed of css selectors

1. ID, e.g. #header
2. Class, e.g. .promo
3. Type, e.g. div
4. Adjacent sibling, e.g. h2 + p
5. Child, e.g. li > ul
6. Descendant, *e.g. ul a*
7. Universal, i.e. *
8. Attribute, e.g. [type="text"]
9. Pseudo-classes/-elements, e.g. a:hover
"""