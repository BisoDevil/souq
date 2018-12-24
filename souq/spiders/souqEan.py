import scrapy


class SouqSpider(scrapy.Spider):
    name = "souq_ean"
    allowed_domains = ["souq.com"]

    with open("urls.txt", "rt") as f:
        search_term = [url.strip() for url in f.readlines()]

    def start_requests(self):
        for key in self.search_term:
            results = 'https://uae.souq.com/ae-en/' + str(key).strip() + '/s/'
            yield scrapy.Request(results, callback=self.parse,
                                 meta={'passed_data': key.strip()})

    def parse(self, response):
        items = {}
        key = response.request.meta['passed_data']
        ean = response.xpath('//dl[@class="stats"]//text()').re('2\d{10,13}')
        title = response.xpath('//div[@class="small-12 columns product-title"]//h1//text()').extract()
        cat = response.xpath('//*').re('(?:product_type":")(.*)(?:","product_category)')
        image = response.xpath(
            "//div[@class='img-bucket']/img/@data-url|//*[contains(@class, 'slider gallary')]//div["
            "2]//img/@data-url|//*[@class='vip-outofstock-item-img-container text-center']/img/@src|//div["
            "@class='img-bucket ']/img/@data-url").extract()
        dessc = response.xpath('//li[@id="description"]//text()').extract()
        items['Original_item'] = key
        items['ean'] = ', '.join(set(ean)).strip()
        items['Title'] = ''.join(title).strip()
        items['Description'] = '\n'.join(dessc).strip()
        items['Category'] = ''.join(cat).strip()
        items['image'] = '\n'.join(image).strip()
        yield items
