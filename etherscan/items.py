# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LabelAddressItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    name_tag = scrapy.Field()
    balance = scrapy.Field()
    txn_count = scrapy.Field()
    label = scrapy.Field()

