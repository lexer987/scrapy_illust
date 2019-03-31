import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # 'https://www.irasutoya.com/search/label/%E3%81%8A%E6%AD%A3%E6%9C%88',
            'https://www.irasutoya.com/p/seasons.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category_list)

    def parse_category_list(self, response):
        for category_page in response.css(".widget-content li a::attr(href)").getall():
            category_page = response.urljoin(category_page)
            yield scrapy.Request(category_page, callback=self.parse_category)

    def parse_category(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        # カテゴリの次のページ
        next_page = response.css('a.blog-pager-older-link::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_category)

        # 画像のあるページ
        for item_page in response.css(".boxim > a::attr(href)"):
            item_page = response.urljoin(item_page.get())
            yield scrapy.Request(item_page, callback=self.parse_item)

    def parse_item(self, response):
        yield {
            'text': response.css(".post h2::text").get(),
            'image': response.css(".entry a::attr(href)").get(),
            'category': response.css(".category a::text").getall()
        }
