import base64
from urllib.request import Request

import scrapy
import datetime
import time

from apteka.items import AptekaItem


def start_requests(self):
    request = Request('https://proxy6.net', callback=self.parse)
    request.meta['proxy'] = 'http://200.10.39.181:8000'
    request.headers['Proxy-Authorization'] = 'Basic ' + base64.encodestring('PoZU01:xpKrUY')
    return request


class AptekaspiderSpider(scrapy.Spider):
    name = "aptekaspider"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = ["https://apteka-ot-sklada.ru/catalog/dieticheskoe-pitanie_-napitki/snizhenie-vesa-pitanie",
        "https://apteka-ot-sklada.ru/catalog/letnie-serii/dlya-zagara",
        "https://apteka-ot-sklada.ru/catalog/tovary-dlya-mamy-i-malysha/butylochki/butylochki-s-rozhdeniya-_0-_",]

    def parse(self, response):
        products = response.css(".ui-card_outlined.goods-card.goods-grid__cell.goods-grid__cell_size_3")
        for product in products:
            next_url = product.css(".goods-card__name.text.text_size_default.text_weight_medium a").attrib['href']
            if 'catalog' in next_url:
                product_url = 'https://apteka-ot-sklada.ru' + next_url
            else:
                product_url = 'https://apteka-ot-sklada.ru' + next_url
            yield scrapy.Request(product_url, callback=self.parse_all)

            next_page = response.css(".ui-pagination__item_next a::attr(href)").get()
            if next_page is not None:
                if "catalog" in next_page:
                    next_page_url = "" + next_page
                else:
                    next_page_url = "https://apteka-ot-sklada.ru" + next_page
                yield response.follow(next_page_url, callback=self.parse)

    def parse_all(self, response):
        product = response.css(".ui-card_outlined.goods-card.goods-grid__cell.goods-grid__cell_size_3")
        product_item = AptekaItem()
        product_item["timestamp"] = time.time() #datetime.datetime.now()
        product_item["RPC"] = response.css(".goods-photo.goods-gallery__picture").attrib['src'][14:23]
        product_item["title"] = response.css("h1 span::text").get()
        product_item["url"] = response.url
        product_item["marketing_tags"] = response.css(".goods-tags__item span::text").get()
        product_item["brand"] = response.xpath("//*[@id='__layout']/div/div[3]/main/header/div[2]/div/span[2]/text()").get()
        product_item["section"] = response.xpath("//main/header/div[1]/ul/li/a/span/span/text()").getall()
        product_item["price_data"] = {
            "current": '',
            "original": response.css(".text_weight_medium.ui-link_theme_primary span span::text").get(),
            "sale_tag": ''
        }
        product_item["stock"] = {
                    "in_stock": response.css(".text_weight_medium.ui-link_theme_primary span::text").get(),
                    "count": response.css(".text_weight_medium.ui-link_theme_primary span::text").get(),
                    }
        product_item["assets"] = {
                    "main_image": 'https://apteka-ot-sklada.ru'+[img.attrib["src"] for img in response.css("img")][2],
                    "set_images": ['https://apteka-ot-sklada.ru'+ img.attrib["src"] for img in response.css("img")][2:4],
                    "view360": '',
                    "video": '',
                    }
        product_item["metadata"] = {
                    "__description": response.xpath('//*[@id="description"]/div/div[1]/div').get(),
                    "АРТИКУЛ": "",
                    "СТРАНА ПРОИЗВОДИТЕЛЬ": response.xpath('//*[@id="__layout"]/div/div[3]/main/header/div[2]/div/span[1]/text()').get(),
                    }
        product_item["variants"] = {}

        yield product_item


