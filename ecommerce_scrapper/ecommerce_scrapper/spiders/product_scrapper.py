import scrapy


class ProductSpider(scrapy.Spider):
    name = "kabum"
    start_url = 'https://www.kabum.com.br/hardware/processadores'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        products = response.xpath('//*[@id="listing"]/article/section/div[3]/div/main/div/a//@href').getall()
        for product in products:
            yield scrapy.Request(url='https://www.kabum.com.br/' + product, callback=self.parse_detail)

    def parse_detail(self, response):
        categories = response.xpath('//*[@id="__next"]/main/article/section/div[1]/div/div//text()').getall()
        categories = categories[1:-3:2]

        title = response.css('h1::text')[0].get()
        price = response.css('h4[itemprop="price"]::text')[0].get()

        price = price[3:]
        price = price.replace(".", "")
        price = price.replace(",", ".")
        price = float(price)

        description = response.css('#description *::text').getall()
        description = ''.join(description)
        
        yield {
            'categories': categories,
            'title': title,
            'price': price,
            'description': description
        }