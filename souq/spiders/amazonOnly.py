import scrapy


class Amazon(scrapy.Spider):
    name = "amazon_asin"
    allowed_domains = ["amazon.com", "amazon.co.uk"]
    # search_term = []

    with open("urls.txt", "rt") as f:
        search_term = [url.strip() for url in f.readlines()]

    #
    custom_settings = {
        'ROBOTSTXT_OBEY': 'False',
        'DOWNLOAD_DELAY': 0.2,
    }

    def start_requests(self):
        i = len(self.search_term)
        for s_term in range(0, i):
            # https://www.amazon.com/dp/B071D11SDP valid asin
            results = 'https://www.amazon.com/dp/' + self.search_term[s_term]
            yield scrapy.Request(results, callback=self.parse,
                                 meta={'passed_data': self.search_term[s_term], 'count': s_term}, dont_filter=True)

    def parse(self, response):
        items = {}
        # title = response.xpath('//span[@id="productTitle"]//text()').extract()
        # checked_title = ''.join(title).strip()
        # if checked_title == '' and response.status == 200:
        #     yield scrapy.Request(response.url, callback=self.parse,
        #                          meta={'passed_data': response.meta['passed_data'], 'count': response.meta['count']},
        #                          dont_filter=True)
        # else:
        #     # response = browser.page_source

        brand = response.xpath('//a[@id="bylineInfo"]/text()|//a[@id="brand"]/@href').extract()
        title = response.xpath('//span[@id="productTitle"]//text()').extract()
        specs_list = response.xpath(
            "//div[@id='feature-bullets']//text()|//div[@id='productDescription']//text()").extract()
        description = response.xpath("//div[@id='productDescription']//text()").extract()
        color = response.xpath('//div[contains(label,"Color")]//span[@class="selection"]//text()').extract()
        # size xpath '//*[@id="twisterJsInitializer_feature_div"]/script/text()'
        size = response.xpath('//*[@id="twisterJsInitializer_feature_div"]/script').re(
            'selected_variations" : {"size_name":.*?."')
        details = response.xpath(
            "//div[@id='detail-bullets']/table/tbody/tr/td[@class='bucket']/div[@class='content']/ul//text()").extract()
        img = response.xpath('//*[@id="imageBlock_feature_div"]/script').re('large.*?.jpg')
        model = response.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li[contains(.,"model")]/span/span[2]/text()').extract()
        asin = response.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li[contains(.,"ASIN")]/span/span[2]/text()').extract()
        cat = response.xpath('//*[@id="dp-container"]/script[5]/text()').re('productTypeName":".*?"')
        material = response.xpath("//div[@id='feature-bullets']//text()").re('[Aa]crylic|[Cc]hiffon|[Cc]orduroy|['
                                                                             'Cc]otton|[Cc]repe|[Dd]enim|['
                                                                             'Ff]lannel|[ '
                                                                             'Gg]abardine|[Gg]eorgette|[Jj]ersey|['
                                                                             'Ll]ace|[Ll]eather|[Ll]inen|[Ll]ycra|['
                                                                             'Mm]ixed Materials|[Nn]ylon|['
                                                                             'Oo]rganza|[ '
                                                                             'Pp]olyester|[Pp]oplin|[Rr]ayon|['
                                                                             'Ss]atin|[Ss]equin|[Ss]ilk|[Ss]uede|['
                                                                             'Tt]affeta|[Tt]oweling|[Vv]elvet|['
                                                                             'Vv]iscose|[Ww]ool')

        # Parsing data to CSV file
        items['Original_Item'] = response.meta['passed_data']
        items['Item_link'] = response.url
        items['Brand'] = ''.join(brand).strip().rsplit('=', 1)[-1]
        items['Title'] = ''.join(title).strip()
        items['Specs'] = ''.join(specs_list).strip().replace(
            '\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\t \n\t\t\t\t\t\t\t', '')
        items['Description'] = ''.join(description).strip().replace(
            '\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\t \n\t\t\t\t\t\t\t', '')
        items['Destails'] = ''.join(details).strip()
        items['Color'] = ''.join(color).strip()
        items['Model'] = ''.join(model).strip()
        items['Material'] = ', '.join(material).strip()
        items['Size'] = ''.join(size).strip().replace('selected_variations" : {"size_name":"', '').replace('"', '')
        items['ASIN'] = ''.join(asin).strip()
        items['Images'] = '\n'.join(img).strip().replace('large":"', '')
        items['Amazon_Category'] = ''.join(cat).strip().replace('productTypeName":', '').replace('"', '')
        print('We are in ' + str(response.meta['count']))
        yield items
