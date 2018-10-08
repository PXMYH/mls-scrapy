# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class CraigbotSpider(scrapy.Spider):
    name = 'craigbot'
    allowed_domains = ['craigslist.ca']
    # TODO: accept search URL from command line
    # tweak start_urls to get to the result faster
    # start_urls = ['https://vancouver.craigslist.ca/search/apa']
    start_urls = ['https://vancouver.craigslist.ca/search/van/apa?min_bedrooms=2&max_bedrooms=2']

    def parse(self, response):
        print ("parsing the response {0}".format(response.body))
        listings = response.xpath('//p[@class="result-info"]')
        print ("\n*************\nlistings: {0}".format(listings))
        for listing in listings:
            # get relative url and construct absolute url
            # relative_url = listing.xpath('a/@href').extract_first()
            # print ("relative url {0}".format(relative_url))
            # absolute_url = response.urljoin(relative_url)

            title = listing.xpath('a[@class="result-title hdrlnk"]/text()').extract_first()
            price = listing.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract()
            neighbourhood = listing.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract()
            area_list = listing.xpath('span[@class="result-meta"]/span[@class="housing"]/text()').extract()

            # processing neighbourhood info
            if neighbourhood:
                neighbourhood = str(neighbourhood[0]).replace('(','').replace(')','').strip()
            else:
                neighbourhood = "UNKNOWN"

            # process space info
            if area_list[0]:
                # remove trailing '-'
                space = str(str(area_list[0]).strip().strip('\n').split('-')[-1]).strip()
                if not space:
                    space = "0ft"
            
            space_num = space.strip('ft')
            if int(space_num) != 0 and space and price:
                unit_price = round(int(str(price[0]).strip('$')) / int(space_num), 1)
            else:
                unit_price = -1

            yield {'Title': title, 'Hood': neighbourhood, 'Price': price, 'Area': space, 'UnitPrice': unit_price}

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        
        yield Request(absolute_next_url, callback=self.parse)
