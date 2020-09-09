# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vul_name = scrapy.Field()
    vul_cnnvd_id = scrapy.Field()
    vul_cve = scrapy.Field()
    vul_date = scrapy.Field()
    vul_solution = scrapy.Field()
    vul_link = scrapy.Field()
    vul_detail_info = scrapy.Field()
    vul_gongji = scrapy.Field()
