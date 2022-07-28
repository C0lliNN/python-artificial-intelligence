import scrapy


class ProductSpider(scrapy.Spider):
    name = "kabum"
    start_url = 'https://www.kabum.com.br/hardware/processadores'

    def start_requests(self):
        urls = [
            'https://www.kabum.com.br/produto/112990/processador-intel-core-i5-10400-cache-12mb-2-9ghz-4-3ghz-max-turbo-lga-1200-bx8070110400',
            'https://www.kabum.com.br/produto/356937/placa-de-video-msi-nvidia-geforce-rtx-3070-gaming-z-trio-8g-8gb-gddr6-lhr-rgb-dlss-ray-tracing-geforce-rtx-3070-gaming-z-trio-8g-lhr',
            'https://www.kabum.com.br/produto/81132/headset-gamer-hyperx-cloud-stinger-drivers-50mm-multiplas-plataformas-p2-e-p3-hx-hscs-bk-na',
            'https://www.kabum.com.br/produto/358110/console-sony-playstation-5-horizon-forbidden-west',
            'https://www.kabum.com.br/produto/115801/controle-sem-fio-ps5-dualsense'            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('main a::attr(href)').getall()[:5]
        for product in products:
            print(product)
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