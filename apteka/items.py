# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AptekaItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field()
    brand = scrapy.Field()
    section = scrapy.Field()
    price_data = scrapy.Field()
    current = scrapy.Field()
    original = scrapy.Field()
    sale_tag = scrapy.Field()
    stock = scrapy.Field()
    in_stock = scrapy.Field()
    count = scrapy.Field()
    assets = scrapy.Field()
    main_image = scrapy.Field()
    set_images = scrapy.Field()
    view360 = scrapy.Field()
    video = scrapy.Field()
    metadata = scrapy.Field()
    __description = scrapy.Field()
    АРТИКУЛ = scrapy.Field()
    СТРАНА_ПРОИЗВОДИТЕЛЬ = scrapy.Field()
    variants = scrapy.Field()
    pass
