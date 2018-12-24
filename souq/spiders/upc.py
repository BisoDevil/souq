# coding=utf-8
import scrapy
from selenium import webdriver

"""
: UPC, EAN, SKU
: Search for search term  in souq.com in all countries
: at first then in Jumia.com and Amazon.
: last step is search for term in bing in souq site at first then
: normal search to get the data from the most of e-commerce website.
"""


class UPC_Loop(scrapy.Spider):
    name = "upc_bktool"
    allowed_domains = ['bing.com', 'souq.com', 'duckduckgo.com', 'jumia.com.eg', 'amazon.com', 'yaoota.com',
                       'google.com', 'amazon.co.uk', 'amazon.ca', 'amazon.in', 'amazon.com.au', 'noon.com']
    # terms = []

    with open("urls.txt", "rt") as f:
        terms = [url.strip() for url in f.readlines()]

    # custom_settings = {
    #     'ROBOTSTXT_OBEY': 'False',
    #     # 'DOWNLOAD_DELAY': .5,
    # }

    def __init__(self, start='none', *args, **kwargs):
        super(UPC_Loop, self).__init__(*args, **kwargs)

        self.start_urls = start

        # search_key = kwargs.get('keyword').split(',')
        # search_start = ['https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords=']
        # # search_end = '&product_cat=0&post_type=product'
        # self.start_urls = [(i + x) for i in search_start for x in search_key]

    def start_requests(self):

        if 'jumia' in self.start_urls:
            for key in self.terms:
                link = 'https://www.jumia.com.eg/catalog/?q=' + key
                yield scrapy.Request(link, callback=self.jumia_prase,
                                     meta={'upc': key})
        elif 'amazon' in self.start_urls:
            for key in self.terms:
                link = 'https://www.amazon.com/s/field-keywords=' + key
                yield scrapy.Request(link, callback=self.amazon_prase,
                                     meta={'upc': key})
        elif 'bing' in self.start_urls:
            for key in self.terms:
                link = 'https://www.bing.com/search?q=' + key
                yield scrapy.Request(link, callback=self.BingSpider,
                                     meta={'upc': key})
        else:
            for key in self.terms:
                results = 'https://uae.souq.com/ae-en/' + str(key).strip() + '/s/'
                yield scrapy.Request(results, callback=self.souq_uae,
                                     meta={'upc': key.strip()})

    def souq_uae(self, response):
        key = response.request.meta['upc']
        links = response.xpath(
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href|//div["
            "@class='col col-info item-content']/a/@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_souq_link,
                                     meta={'upc': key, 'web_source': 'SOUQ_UAE'})
        else:
            link = 'https://egypt.souq.com/eg-en/' + key + '/s/'
            yield scrapy.Request(link, callback=self.souq_egy,
                                 meta={'upc': key})

    def souq_egy(self, response):
        key = response.request.meta['upc']
        links = response.xpath(
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href|//div["
            "@class='col col-info item-content']/a/@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_souq_link,
                                     meta={'upc': key, 'web_source': 'SOUQ_EGY'})
        else:
            link = 'https://saudi.souq.com/sa-en/' + key + '/s/'
            yield scrapy.Request(link, callback=self.souq_ksa,
                                 meta={'upc': key})

    def souq_ksa(self, response):
        key = response.request.meta['upc']
        links = response.xpath(
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href|//div["
            "@class='col col-info item-content']/a/@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_souq_link,
                                     meta={'upc': key, 'web_source': 'SOUQ_KSA'})
        else:
            # If No result in all country go to bing with passed upc
            link = 'https://www.amazon.com/s/field-keywords=' + key
            yield scrapy.Request(link, callback=self.amazon_prase,
                                 meta={'upc': key})

    # Parse data from souq.com single link
    def parse_souq_link(self, response):
        key = response.request.meta['upc']
        web_source = response.request.meta['web_source']
        item = DataItem()
        page = response.xpath("//*").extract()
        compare = ''.join(page)
        if key in compare:
            url = response.request.url
            ean = response.xpath("//dt[.='Item EAN']/following::dd[1]/text()").extract()
            brand = response.xpath("//div[@class='small-12 columns product-title']/span[1]/a[1]/text()").extract()
            title = response.xpath('//div[@class="small-12 columns product-title"]//h1//text()').extract()
            price = response.xpath("//h3[@class='price is sk-clr1']/text()").extract()
            itemtype = response.xpath('//*').re('(?<=bannerItemTypeName: \').*(?=\',)')[0]
            asin = response.xpath(
                "//dl/dt[.='EAN-13']/following-sibling::dd[1]/text()|//dl/dt[.='UPC-A']/following-sibling::dd[1]/text()").extract()
            item['a_Main_queries'] = ''.join(key).strip()
            item['b_Web_Source'] = web_source
            item['d_ASIN_EAN_SKU'] = ', '.join(set(ean)).strip()
            item['c_URL'] = url
            item['c_Brand'] = ''.join(brand).strip()
            item['e_Product_Title'] = ''.join(title).strip()
            item['f_Price'] = ''.join(price).strip()
            item['k_item_type'] = ''.join(itemtype).strip()
            item['j_UPC_EAN_13'] = ', '.join(asin).strip()
            item['k_Status'] = response.status
            yield item
        else:
            item = DataItem()
            ean = response.xpath("//dt[.='Item EAN']/following::dd[1]/text()").extract()
            item['a_Main_queries'] = ''.join(key).strip()
            item['c_URL'] = response.url
            item['d_ASIN_EAN_SKU'] = ', '.join(set(ean)).strip()
            item['b_Web_Source'] = 'Close to correct'
            item['k_Status'] = response.status
            yield item

    def jumia_prase(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//section[@class='products']//@href|//a[@class='link']/@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_jumia_link,
                                     meta={'upc': key, 'web_source': 'JUMIA'})
        else:
            link = 'https://www.noon.com/en-ae/search?q=' + key

            yield scrapy.Request(link, callback=self.noon_parse,
                                 meta={'upc': key})

    def noon_parse(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//a[@class='jsx-2342377652 product gridView']//@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_noon_link,
                                     meta={'upc': key, 'web_source': 'NOON'})
        else:

            link = 'https://www.bing.com/search?q=' + key
            yield scrapy.Request(link, callback=self.BingSpider,
                                 meta={'upc': key})

    def parse_noon_link(self, response):
        key = response.request.meta['upc']
        web_source = response.request.meta['web_source']
        item = DataItem()
        page = response.xpath("//*").extract()
        compare = ''.join(page)
        if key in compare:
            url = response.request.url
            item['a_Main_queries'] = ''.join(key).strip()
            item['b_Web_Source'] = web_source
            yield item

        else:
            item = DataItem()
            item['a_Main_queries'] = ''.join(key).strip()
            item['c_URL'] = response.url
            item['b_Web_Source'] = 'Close to correct'
            item['k_Status'] = response.status
            yield item

    # Parse data from Jumia single link
    def parse_jumia_link(self, response):
        key = response.request.meta['upc']
        web_source = response.request.meta['web_source']
        item = DataItem()
        page = response.xpath("//*").extract()
        compare = ''.join(page)
        if key in compare:
            url = response.request.url
            sku = response.xpath("//div[div[1][contains(.,'SKU')]]/div[2]/text()").extract()
            itemType = response.xpath("//a[@class='jsx-3046124812 crumb'][last()]/text()").extract()
            brand = response.xpath("//a[@class='jsx-692826563 brand']/text()").extract()
            title = response.xpath("//h1[@class='jsx-692826563']/text()").extract()
            price = response.xpath(
                "//p[@class='jsx-996473556 productPrice large']/span[@class='jsx-996473556 sellingPrice']/text()").extract()
            key_feature = response.xpath("//div[@class='jsx-3205765686 container']/text()").extract()
            description = response.xpath("//div[@class='jsx-3839513811 container']/text()").extract()
            model = response.xpath("//div[div[1][.='Model']]/div[2]/text()").extract()
            img = response.xpath("//img[@class='jsx-57666071']/@src").extract()
            item['a_Main_queries'] = ''.join(key).strip()
            item['b_Web_Source'] = web_source
            item['d_ASIN_EAN_SKU'] = ''.join(sku).strip()
            item['c_Brand'] = ''.join(brand).strip()
            item['c_URL'] = url
            item['k_item_type'] = ''.join(itemType).strip()
            item['e_Product_Title'] = ''.join(title).strip()
            item['f_Price'] = ''.join(price).strip()
            item['h_Description'] = ''.join(description).strip()
            item['g_Details_Specs'] = '\n'.join(key_feature).strip()
            item['j_UPC_EAN_13'] = ''.join(model).strip()
            item['i_Images'] = '\n'.join(img).strip()
            item['k_Status'] = response.status
            yield item
        else:
            item = DataItem()
            item['a_Main_queries'] = ''.join(key).strip()
            item['c_URL'] = response.url
            item['b_Web_Source'] = 'Close to correct'
            item['k_Status'] = response.status
            yield item

    def amazon_prase(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//ul[@id='s-results-list-atf']/li/div/div/div/div[1]/div/div/a/@href").extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_amazon_link,
                                     meta={'upc': key, 'web_source': 'AMAZON'})
        else:
            # If No result in all country go to bing with passed upc
            link = 'https://www.jumia.com.eg/catalog/?q=' + key
            yield scrapy.Request(link, callback=self.jumia_prase,
                                 meta={'upc': key})

    # Parse data from Amazon single link.
    def parse_amazon_link(self, response):
        key = response.request.meta['upc']
        web_source = response.request.meta['web_source']
        item = DataItem()
        page = response.xpath("//*").extract()
        upc = response.xpath("//*").re(''.join(key).strip())
        compare = ''.join(page).strip()
        if key in compare:
            url = response.request.url
            brand = response.xpath('//a[@id="bylineInfo"]/text()|//a[@id="brand"]/@href').extract()
            cat = response.xpath('//*[@id="dp-container"]/script[5]/text()').re('productTypeName":".*?"')
            asin = response.xpath(
                "//li[b[1][contains(.,'ASIN')]]//text()|//tr[td[1][contains(.,'ASIN')]]/td[2]//text()|//tr[th[1]["
                "contains(.,'ASIN')]]/td[1]//text()").extract()
            title = response.xpath("//span[@id='productTitle']//text()").extract()
            price = response.xpath(
                "//span[@class='price']/text()|//span[@class='price -no-special']/span/text()").extract()
            details = response.xpath(
                "//div[@id='fbExpandableSectionContent']/ul//text()|//div[@id='iframeContent']//text()|//div["
                "@id='feature-bullets']/ul//text()").extract()
            description = response.xpath("//div[@id='productDescription']//text()").extract()
            img = response.xpath('//*[@id="imageBlock_feature_div"]/script').re('large.*?.jpg')
            item['a_Main_queries'] = ''.join(key).strip()
            item['b_Web_Source'] = web_source
            item['c_Brand'] = ''.join(brand).strip()
            item['k_item_type'] = ''.join(cat).strip().replace('productTypeName":', '').replace('"', '')
            item['d_ASIN_EAN_SKU'] = ''.join(asin).strip()
            item['c_URL'] = url
            item['e_Product_Title'] = ''.join(title).strip()
            item['f_Price'] = ''.join(price).strip()
            item['h_Description'] = ''.join(description).strip().replace(
                '\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\t \n\t\t\t\t\t\t\t', '')
            item['g_Details_Specs'] = '\n'.join(details).strip()
            item['j_UPC_EAN_13'] = ', '.join(set(upc)).strip()
            item['i_Images'] = '\n'.join(img).strip().replace('large":"', '')
            item['k_Status'] = response.status
            yield item
        else:
            item = DataItem()
            item['a_Main_queries'] = ''.join(key).strip()
            item['c_URL'] = response.url
            item['b_Web_Source'] = 'Close to correct'
            item['k_Status'] = response.status
            yield item

    # Parse Yaoota link
    def parse_yaoota_link(self, response):
        key = response.request.meta['upc']
        web_source = response.request.meta['web_source']
        item = DataItem()
        page = response.xpath("//*").extract()
        upc = response.xpath("//*").re(''.join(key).strip())
        compare = ''.join(page)
        if key in compare:
            url = response.request.url
            title = response.xpath("//h1[@class='productHeader__content__title']//text()").extract()
            price = response.xpath("//span[@class='number']/text()").extract()
            description = response.xpath(
                "//div[@class='productSection productSection--description col-md-12']//text()").extract()
            img = response.xpath('//div[@class="productHeader__gallery__large__imgCont"]//img//@src').extract()
            item['a_Main_queries'] = ''.join(key).strip()
            item['b_Web_Source'] = web_source
            item['c_URL'] = url
            item['e_Product_Title'] = ''.join(title).strip()
            item['f_Price'] = ''.join(price).strip()
            item['h_Description'] = ''.join(description).strip()
            item['j_UPC_EAN_13'] = upc
            item['i_Images'] = '\n'.join(img).strip()
            item['k_Status'] = response.status
            yield item
        else:
            link = 'https://www.bing.com/search?q=' + key
            yield scrapy.Request(link, callback=self.BingSpider,
                                 meta={'upc': key})

    def BingSpider(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//ol[@id='b_results']/li[@class='b_algo']/h2/a/@href").extract()
        if len(links) > 0:
            if ('souq.com' or 'jumia.com' or 'amazon.com') in ', '.join(links).strip():
                for link in links:
                    if 'souq.com' in link:
                        yield scrapy.Request(link, callback=self.parse_souq_link,
                                             meta={'upc': key, 'web_source': 'SOUQ'}, dont_filter=True)
                        break
                    elif 'amazon.com' in link:
                        yield scrapy.Request(link, callback=self.parse_amazon_link,
                                             meta={'upc': key, 'web_source': 'AMAZON'}, dont_filter=True)
                    elif 'jumia.com' in link:
                        yield scrapy.Request(link, callback=self.parse_jumia_link,
                                             meta={'upc': key, 'web_source': 'JUMIA'}, dont_filter=True)
            else:
                link = 'https://www.google.com/search?q=' + key
                yield scrapy.Request(link, callback=self.google_spider, meta={'upc': key})
        else:
            link = 'https://www.google.com/search?q=' + key
            yield scrapy.Request(link, callback=self.google_spider, meta={'upc': key})

    def google_spider(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//h3/a/@href|//div[@class='r']/a/@href").extract()

        if response.status == 503 or ('ipv4' or 'sorry') in response.request.url:
            # Google spider
            links = go_search_souq(key)
            if len(links) > 0:
                if ('souq.com' or 'jumia.com' or 'amazon.com') in ', '.join(links).strip():
                    for link in links:
                        link.replace('/url?url=', '')
                        if 'souq' in link:
                            yield scrapy.Request(link, callback=self.parse_souq_link,
                                                 meta={'upc': key, 'web_source': 'SOUQ'}, dont_filter=True)
                            break
                        elif 'amazon' in link:
                            yield scrapy.Request(link, callback=self.parse_amazon_link,
                                                 meta={'upc': key, 'web_source': 'AMAZON'}, dont_filter=True)
                            break
                        elif 'jumia' in link:
                            yield scrapy.Request(link, callback=self.parse_jumia_link,
                                                 meta={'upc': key, 'web_source': 'JUMIA'}, dont_filter=True)
                            break
                else:
                    item = DataItem()
                    item['a_Main_queries'] = ''.join(key).strip()
                    item['c_URL'] = '\n'.join(links).strip()
                    item['b_Web_Source'] = 'Google'
                    item['k_Status'] = response.status
                    yield item
            else:
                item = DataItem()
                item['a_Main_queries'] = ''.join(key).strip()
                item['c_URL'] = "Item doesn't exist in search engine"
                item['b_Web_Source'] = 'Google'
                item['k_Status'] = response.status
                yield item
        # yield scrapy.Request(link, callback=self.GoogleSpider,  meta = {'upc': key})
        else:
            if len(links) > 0:
                if ('souq.com' or 'jumia.com' or 'amazon') in ', '.join(links).strip():
                    for link in links:
                        if 'souq.com' in link:
                            yield scrapy.Request(link, callback=self.parse_souq_link,
                                                 meta={'upc': key, 'web_source': 'SOUQ'}, dont_filter=True)
                            break
                        elif 'amazon.com' in link:
                            yield scrapy.Request(link, callback=self.parse_amazon_link,
                                                 meta={'upc': key, 'web_source': 'AMAZON'}, dont_filter=True)
                        elif 'jumia.com' in link:
                            yield scrapy.Request(link, callback=self.parse_jumia_link,
                                                 meta={'upc': key, 'web_source': 'JUMIA'}, dont_filter=True)
                else:
                    item = DataItem()
                    item['a_Main_queries'] = ''.join(key).strip()
                    item['c_URL'] = '\n'.join(links).strip()
                    item['b_Web_Source'] = 'Google'
                    item['k_Status'] = response.status
                    yield item
            else:
                item = DataItem()
                item['a_Main_queries'] = ''.join(key).strip()
                item['c_URL'] = "Item doesn't exist in search engine"
                item['b_Web_Source'] = 'Google'
                item['k_Status'] = response.status
                yield item


def go_search_souq(search_term):
    url = 'https://www.google.com/?hl=en'
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome('./webdrivers/chromedriver.exe')
    browser.get(url)
    search_box = browser.find_element_by_name('q')
    search_box.send_keys(search_term)
    search_box.submit()

    # time.sleep(2)

    # try:
    #     links = browser.find_elements_by_xpath('//h3/a[contains(@href, "/i/") or contains(@href, "/u/")]')
    # except:
    links = browser.find_elements_by_xpath("//h3/a|//div[@class='r']/a")

    results = []
    for link in links:
        href = link.get_attribute('href')

        results.append(href)
        # break

    # print(results)
    browser.close()
    return results


class DataItem(scrapy.Item):
    a_Main_queries = scrapy.Field()
    b_Web_Source = scrapy.Field()
    c_URL = scrapy.Field()
    c_Brand = scrapy.Field()
    d_ASIN_EAN_SKU = scrapy.Field()
    e_Product_Title = scrapy.Field()
    f_Price = scrapy.Field()
    g_Details_Specs = scrapy.Field()
    h_Description = scrapy.Field()
    i_Images = scrapy.Field()
    j_UPC_EAN_13 = scrapy.Field()
    k_item_type = scrapy.Field()
    k_Status = scrapy.Field()
