import scrapy
from scrapy_selenium import SeleniumRequest
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_article_node(self, article_id, header, author, date_published, link, text):
        with self.driver.session() as session:
            session.run(
                "MERGE (a:Article {id: $article_id}) "
                "ON CREATE SET a.header = $header, a.author = $author, a.date_published = $date_published, a.link = $link, a.text = $text",
                article_id=article_id, header=header, author=author, date_published=date_published, link=link, text=text)

    def create_relationship(self, from_id, to_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (a:Article {id: $from_id}), (b:Article {id: $to_id}) "
                "MERGE (a)-[:REFERENCES]->(b)",
                from_id=from_id, to_id=to_id)

class TimeSpider(scrapy.Spider):
    name = "time"
    max_depth = 3  # deepest layer the spider should scrape 

    def __init__(self, search_term=None, *args, **kwargs):
        super(TimeSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term

    def start_requests(self):
        search_term = self.search_term
        start_urls = [f'https://time.com/search/?q={search_term}']
        for url in start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_search_results, meta={'depth': 1})

    def parse_search_results(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve search results: {response.url} with status {response.status}")
            return

        articles = response.css('article.partial.tile.media.image-top.search-result')
        if not articles:
            self.logger.warning(f"No articles found on search results page: {response.url}")

        for article in articles:
            article_link = article.css('div.headline a::attr(href)').get()
            if article_link:
                yield SeleniumRequest(url=article_link, callback=self.parse_article, meta={'depth': response.meta['depth'] + 1})



    def parse_article(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve article: {response.url} with status {response.status}")
            return

        header = response.css('h1::text').get()
        link_to_article = response.url
        depth = response.meta['depth']

        if depth > self.max_depth:
            self.logger.info(f"Reached maximum depth of {self.max_depth} for link: {link_to_article}")
            return

        dates = response.css('time::text').getall()
        date = " | ".join(dates)
        if not date:
            date = response.css('span.entry-date::text').get()  # accounting for different Time website formats

        author = response.css('a[href*="/author/"]::text').get()

        paragraphs = response.css('p').xpath('string(.)').getall()
        full_text = " ".join(paragraphs)

        nested_links = response.css('p a::attr(href)').getall()  # nested links are <a> tags within <p> tags
        nested_links = [response.urljoin(url) for url in nested_links]

        cant_be_scraped = [] #to get a sense of how many links outside of the general time format
        filtered_links = []
        self.logger.info(f"These links could not be scraped: {cant_be_scraped}")

        for link in nested_links:
            if (link.startswith('http://time.com/') or link.startswith('https://time.com/')) and ('/tag/' not in link) :
                filtered_links.append(link)
            else:
                cant_be_scraped.append(link)

        yield {
            'type': 'article',
            'header': header,
            'author': author,
            'update_date/publish_date': date,
            'link_to_article': link_to_article,
            'text': full_text,
            'nested_links': filtered_links,
        }

        for nested_link in filtered_links:
            yield SeleniumRequest(url=nested_link, callback=self.parse_article, meta={'depth': depth + 1})
"""
------------------DEBUGGING UTILITY-----------------------------------------------      

 with open('rendered_response.html', 'w', encoding='utf-8') as f:
    #f.write(response.text)  

-------------------------USEFUL----------------------------------------------------
Speed of css selectors***********************

1. ID, e.g. #header
2. Class, e.g. .promo
3. Type, e.g. div
4. Adjacent sibling, e.g. h2 + p
5. Child, e.g. li > ul
6. Descendant, *e.g. ul a*
7. Universal, i.e. *
8. Attribute, e.g. [type="text"]
9. Pseudo-classes/-elements, e.g. a:hover

neo4j auth***********

NEO4J_URI=neo4j+s://d0e8bb89.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=wN2ZcdiQ8NkfUciltN1kCwdSUQO7fz7x18XuFqL9rW0
AURA_INSTANCEID=d0e8bb89
AURA_INSTANCENAME=Instance01        

for pages after the first in search results*************

if pagination is needed, uncomment and use below
    for i in range(2, 4):
    next_page_url = f'https://time.com/search/?q={self.search_term}&page={i}'
    yield SeleniumRequest(url=next_page_url, callback=self.parse_search_results, meta={'depth': response.meta['depth']})
"""