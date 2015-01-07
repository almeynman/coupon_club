# -*- coding: utf-8 -*-
import re

from datetime import datetime
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from coupon_scraper.items import MyItem

    # mb put this in utils both support functions
def clean_extract(selector, path_of_info, path='xpath'):
    try:
        if 'css' in path:
            clean_value = selector.css(path_of_info).extract()[0]
        else:
            clean_value = selector.xpath(path_of_info).extract()[0]
    except:
        clean_value = ''
    # self.log('clean_value="" for \nxpath: %s\n count: %d\n item: %s' % (xpath_of_info, count, self.items[count]))
    clean_value = clean_value.strip()
    return clean_value

def get_numbers_from_string(string):
    numbers_list = re.findall('\d+', string.replace(' ', ''))
    if numbers_list:
        return numbers_list[0]
    else:
        return 0


class MySpider(Spider):
    name = 'chocolife'
    allowed_domains = [
        'chocolife.me'
    ]
    start_urls = [
        'http://www.chocolife.me',
    ]

    def parse(self, response):
        sel = Selector(response)
        deals = sel.xpath('//li[@class="b-deal"]')

        for deal in deals[:5]:
            item = MyItem()
            # need to finish
            categories = clean_extract(
                deal,
                './/@data-categories',
            )
            raw_discount = clean_extract(
                deal, 
                './/span[@class="e-deal__discount"]/text()', 
            )
            item['discount'] = get_numbers_from_string(raw_discount)
            item['title'] = clean_extract(
                deal, 
                './/h2[@class="e-deal__title"]/text()', 
            )
            item['summary_front'] = clean_extract(
                deal, 
                './/p[@class="e-deal__text"]/text()', 
            )
            raw_number_of_purchases = clean_extract(
                deal, 
                './/span[@class="e-deal__link"]/text()', 
            )
            item['number_of_purchases'] = get_numbers_from_string(raw_number_of_purchases)
            item['image_url'] = 'http://www.chocolife.me' + clean_extract(
                deal,
                './/img[@class="e-deal__img lazy"]/@data-original', 
            )
            raw_old_price = clean_extract(
                deal,
                './/span[@class="e-deal__price e-deal__price--old "]/text()',
            )
            item['old_price'] = get_numbers_from_string(raw_old_price)
            raw_new_price = clean_extract(
                deal,
                './/span[@class="e-deal__price "]/text()',
            )
            item['new_price'] = get_numbers_from_string(raw_new_price)
            item['deal_url'] = clean_extract(
                deal,
                './/a[@class="e-link--deal"]/@href',
            )
            request = Request(
                item['deal_url'],
                callback=self.parse_deal_info
            )
            request.meta['item'] = item
            yield request


    def parse_deal_info(self, response):
        item = response.meta['item']
        sel = Selector(response)
        # item['address'] = clean_extract(
        #     sel,
        #     '//li[@class="e-offer__feature "]/text()', 
        # )
        # item['info'] = clean_extract(
        #     sel,
        #     './/p[@class="e-offer__description"]/text()',
        # )
        item['conditions'] = clean_extract(
            sel,
            './/ul[@class="b-conditions-list"',
        )
        item['website'] = 'www.chocolife.kz'
        # raw_end_timestamp = clean_extract(
        #     sel,
        #     'p.js-e-offer__expire-date ::text',
        #     'css'
        # )
        # if raw_end_timestamp != '':
        #     item['end_timestamp'] = int(raw_end_timestamp) / 1000
        # else:
        #     item['end_timestamp'] = 0

        # address_path = sel.css(':contains("%s")' % u'г. Алматы')
        # if '<b>' in address_path.extract() and len(address_path.extract())<200:
        #     item['address'] = address_path.extract()
        # else:
        #     item['address'] = 'ok'


            # some = address_path.xpath('.//text()[name(..)="b"').extract()
        # offer_features = sel.css('ul.b-offer__features-list li')
        # if len(offer_features) > 1:
        #     item['address'] = offer_features[0].xpath('b/text').extract()
        yield item
        # print item['address']
        # print item['end_timestamp']