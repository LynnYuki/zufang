# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 房屋描述
    pattern = scrapy.Field()
    # 租房方式类别
    type = scrapy.Field()
    # 房屋地址
    address = scrapy.Field()
    # 图片地址
    img = scrapy.Field()


