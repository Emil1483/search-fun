import scrapy


class DroneSpiderSpider(scrapy.Spider):
    name = 'drone_spider'
    allowed_domains = ['jessops.com/drones']
    start_urls = ['http://jessops.com/drones/']

    def parse(self, response):
        products = response.css('div.details-pricing')
        for product in products:
            name = product.css('a::text').get()
            price = product.css('p.price.larger::text').get()
            price = price.replace(',', '')
            yield {
                'name': name,
                'price': price,
            }
            
# TODO: maybe watch this https://www.youtube.com/watch?v=o1g8prnkuiQ&t=1