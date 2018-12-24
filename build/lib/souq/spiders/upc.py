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
                       'google.com', 'amazon.co.uk', 'amazon.ca', 'amazon.in', 'amazon.com.au']
    terms = ['800897834722', '800897832803', '800897832810', '800897831547', '800897077907', '800897840235',
             '800897840242', '800897840297', '800897840327', '800897822187', '800897822156', '800897016142',
             '800897016166', '800897016173', '800897848408', '632592538933', '800897077839', '800897848286',
             '800897077884', '800897077952', '800897840280', '800897809041', '800897016203', '800897832797',
             '800897809898', '800897017125', '800897017132', '800897839819', '800897084943', '800897084950',
             '800897084974', '800897084998', '800897085001', '800897824204', '800897093228', '800897141431',
             '800897824273', '800897155285', '800897017149', '800897155308', '4052136031003', '800897833213',
             '800897155278', '4051564351868', '800897103125', '4052136006452', '800897155261', '800897103156',
             '4051564352506', '4052136003345', '800897155254', '800897103200', '4051564035508', '4019674330333',
             '800897017620', '800897103101', '4051564003613', '4019674483039', '6253503293354', '800897017644',
             '800897840273', '4051564003712', '4052136001877', '4019674013045', '800897849221', '4051564037106',
             '6253503293224', '4019674492185', '4019674483107', '800897103132', '4051564037038', '6253503293590',
             '4019674049235', '4019674485170', '800897822958', '4051564037052', '6253503290674', '4019674049273',
             '4019674049730', '800897822897', '4051564037076', '6253503293033', '4019674049754', '4052136001464',
             '800897840204', '4051564372016', '6253503293019', '4019674028179', '800897105617', '4019674049792',
             '4051564372023', '6291106031133', '4019674046159', '800897016197', '4019674049778', '4051564381018',
             '4019674046180', '800897016159', '6291106031102', '4019674497081', '4051564383081', '4019674046197',
             '6291106030853', '800897016180', '4019674497012', '4051564440036', '4052136037685', '6291106030785',
             '4051564440067', '800897093242', '4019674330166', '4052136037692', '6291106030839', '800897098179',
             '4052136009484', '4051564440104', '6291106030778', '800897098186', '4019674330296', '4019674483053',
             '4051564440142', '6291106030815', '800897098094', '4052136046649', '4019674330197', '4051564001756',
             '800897098100', '4052136050851', '4051564002227', '6291106030754', '4019674330074', '4052136050691',
             '800897098117', '4051564002258', '4019674330180', '6291106031126', '4052136050882', '800897098124',
             '4051564002302', '4019674330135', '773602070299', '4052136050899', '800897098155', '4051564002319',
             '4019674330302', '773602475131', '4052136058642', '800897098087', '4051564001015', '4019674330111',
             '773602484867', '4052136058604', '800897098162', '4051564001619', '773602484898', '4019674330326',
             '4052136058611', '800897011994', '4051564001626', '773602475209', '4019674330258', '800897012007',
             '4051564001633', '4052136059328', '773602458134', '4019674330449', '4052136058307', '4051564003781',
             '773602070374', '800897012014', '4019674172186', '4052136058314', '800897012045', '4051564000933',
             '773602046522', '4019674172179', '4052136058321', '800897832827', '773602046430', '4051564000940',
             '4019674172193', '4052136058338', '800897849252', '4051564000957', '6283503293962', '4019674172124',
             '4052136055085', '800897096489', '6283503293948', '4051564003460', '4019674049228', '4052136058352',
             '800897018184', '4051564003477', '6283503293924', '4019674492215', '4052136058369', '4051564383012',
             '800897146184', '6283503293917', '4019674492154', '4052136055078', '800897140342', '4051564383166',
             '6283503293900', '4019674049280', '4051564231023', '800897140373', '4052136058383', '7290015295734',
             '4019674029640', '800897140366', '4052136055061', '4051564231245', '6253503291107', '4019674221150',
             '4051564006089', '800897140380', '4052136055092', '6253503293170', '4019674221204', '4051564005686',
             '800897140397', '4052136055047', '6253503293057', '4019674032411', '4051564005860', '800897824853',
             '6253503293156', '4019674030844', '4052136058406', '4051564005877', '800897832834', '6253503291251',
             '4019674250013', '4051564005884', '4052136050677', '800897832162', '6253503291312', '4019674250037',
             '4051564006355', '800897151300', '6253503291305', '4052136050837', '4019674032930', '800897098353',
             '6253503291244', '4051564006362', '4052136009330', '4019674028223', '800897012021', '6253503291268',
             '4051564005662', '4052136039283', '4019674221235', '800897824242', '4051564006263', '6253503291220',
             '4052136058659', '4019674028124', '6253503291299', '4051564012998', '800897824297', '4052136047653',
             '4019674049617', '6253503291206', '4051564016422', '4052136001495', '4019674041338', '4051564016439',
             '6253503293163', '4019674485286', '4019674041062', '4051564012806', '4052136058390', '6253503291275',
             '4051564015906', '4019674041130', '4052136058413', '6253503291213', '4051564012813', '4019674172117',
             '4052136057423', '3378872108542', '4019674049761', '4051564012820', '4052136056303', '3378872099970',
             '4019674028261', '4051564012837', '4052136056310', '3378872117056', '4019674483183', '4051564012844',
             '4052136059144', '3378872099987', '4019674028018', '4051564016965', '4052136058291', '3378872117001',
             '4019674330340', '4051564016972', '4052136059847', '3378872099932', '4019674202012', '4051564016897',
             '4052136060584', '3378872099963', '4019674172568', '4051564016903', '4052136060591', '3378872099956',
             '4019674172100', '4051564016910', '4052136058376', '3378872108535', '4019674028032', '4051564016941',
             '4052136065435', '3378872108481', '4019674030042', '4051564016958', '4052136049053', '3378872103905',
             '4019674250082', '4051564015265', '4052136049060', '3378872055617', '4019674281161', '4052136059151',
             '3378872088110', '4051564016224', '4019674240038', '4052136056396', '3378872088165', '4051564016279',
             '4052136005202', '4052136039429', '4051564016286', '3378872088172', '4019674028230', '4052136057881',
             '3378872088189', '4051564016293', '4019674028254', '4051564201781', '4051564000995', '3378872103929',
             '4019674485101', '4051564020580', '3378872104063', '4051564016880', '4019674485125', '3378872104070',
             '4051564020948', '4051564013407', '3378872104087', '4052136006650', '4051564231351', '4051564016309',
             '3378872104094', '4052136006667', '4051564231429', '4051564016453', '3378872104117', '4052136001976',
             '4051564023185', '4051564016477', '3378872109594', '4052136006940', '4051564023369', '3380810119367',
             '3378872109617', '4052136030013', '4051564023383', '96200002661', '3378872109624', '4051564023390',
             '4052136030273', '96200208117', '3378872109631', '4051564023819', '4052136005691', '96200208131',
             '3378872109648', '4052136005707', '4051564351028', '3378872110392', '96200204430', '4052136005714',
             '4051564351219', '3378872110408', '96200208162', '4052136031447', '4051564351356', '3378872110415',
             '4052136031249', '4051564351417', '3378872110439', '96200208179', '4051564351479', '3378872110446',
             '4052136031454', '96200208186', '4051564351707', '3378872110453', '963952', '4051564351790',
             '3378872110521', '969492', '3378872108504', '7640107016028', '3378872108559', '3378872108511',
             '3378872099642', '3378872100225', '3378872108498', '3378872108528']

    # with open("urls.txt", "rt") as f:
    #     terms = [url.strip() for url in f.readlines()]

    # custom_settings = {
    #     'ROBOTSTXT_OBEY': 'False',
    #     # 'DOWNLOAD_DELAY': .5,
    # }

    def __init__(self, start='none', *args, **kwargs):
        super(UPC_Loop, self).__init__(*args, **kwargs)

        self.start_urls = start

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
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href").extract()
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
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href").extract()
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
            "//div[@class='columns small-7 medium-12']//a//@href|//a[contains(@id,'quickview')]/@href").extract()
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
            link = 'https://www.bing.com/search?q=' + key
            yield scrapy.Request(link, callback=self.BingSpider,
                                 meta={'upc': key})

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
            itemType = response.xpath("//nav[@class='osh-breadcrumb']/ul/li[last()-2]/a/text()").extract()
            brand = response.xpath("//div[@class='sub-title'][contains(text(),'By')]/a/text()").extract()
            title = response.xpath("//h1[@class='title']/text()").extract()
            price = response.xpath(
                "//span[@class='price']/text()|//span[@class='price -no-special']/span/text()").extract()
            key_feature = response.xpath("//div[@class='detail-features']/div[2]/ul//text()").extract()
            description = response.xpath("//div[@class='product-description']/text()").extract()
            model = response.xpath("//div[div[1][.='Model']]/div[2]/text()").extract()
            img = response.xpath("//div[@id='thumbs-slide']//@href").extract()
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
            img = response.xpath("//div[@id='imgTagWrapperId']/img/@data-old-hires").extract()
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
                item = DataItem()
                item['a_Main_queries'] = ''.join(key).strip()
                item['c_URL'] = '\n'.join(links).strip()
                item['b_Web_Source'] = 'Bing'
                item['k_Status'] = response.status
                yield item
        else:
            link = 'https://www.google.com/search?q=' + key
            yield scrapy.Request(link, callback=self.google_spider, meta={'upc': key})

    def google_spider(self, response):
        key = response.request.meta['upc']
        links = response.xpath("//h3/a/@href").extract()

        if 'ipv4' in response.url:
            # Google spider
            links = go_search_souq(key)
            if len(links) > 0:
                if ('souq.com' or 'jumia.com' or 'amazon.com') in ', '.join(links).strip():
                    for link in links:
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
    links = browser.find_elements_by_xpath('//h3/a')

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
