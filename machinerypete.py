import scrapy


class MachinerypeteSpider(scrapy.Spider):
    name = 'machinerypete'
    allowed_domains = ['www.machinerypete.com']
    start_urls = ['https://www.machinerypete.com/dealerships/search']

    def parse(self, response):
        links = response.css(
            'div.row > div > a.btn.btn-default.btn-xs::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_dealers)

    def parse_dealers(self, response):
        dealers = response.css(
            'div.row > div > ul > li > a::attr(href)').getall()
        for dealer in dealers:
            dealer = response.urljoin(dealer)
            yield scrapy.Request(url=dealer, callback=self.parse_contact)

    def parse_contact(self, response):
        yield {
            'email': response.css('div.store-item::text').getall()[3],
            'phone': response.css('div.store-item > a::text').getall()[-1],
            'address': f"{response.css('div.store-item::text').getall()[4]}, {response.css('div.store-item::text').getall()[5]}"
        }
