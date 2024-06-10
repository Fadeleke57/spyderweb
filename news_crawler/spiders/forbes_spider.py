import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForbesSpider(scrapy.Spider):
    name = "forbesTest"
    search_term = "technology"

    def start_requests(self):
        url = f'https://www.forbes.com/search/?q={self.search_term}'
        yield SeleniumRequest(url=url, callback=self.parse_search_results, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'div.CardArticle_wrapper__MpbGX')))

    def parse_search_results(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve search results: {response.url} with status {response.status}")
            return

        with open('rendered_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        articles = response.css('div.CardArticle_wrapper__MpbGX') 
        if not articles:
            self.logger.warning(f"No articles found on search results page: {response.url}")
