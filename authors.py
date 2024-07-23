import scrapy
import json

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    authors = []

    def parse(self, response):
        author_urls = response.css('div.quote span a::attr(href)').getall()
        for url in author_urls:
            yield response.follow(url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author = {
            'name': response.css('h3.author-title::text').get(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'bio': response.css('div.author-description::text').get().strip(),
        }
        self.authors.append(author)

    def close(self, reason):
        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(self.authors, f, ensure_ascii=False, indent=4)
