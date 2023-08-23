import scrapy
import datetime


class AptekaspiderSpider(scrapy.Spider):
    name = "aptekaspider"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = ["https://apteka-ot-sklada.ru/catalog/dieticheskoe-pitanie_-napitki/snizhenie-vesa-pitanie",
        "https://apteka-ot-sklada.ru/catalog/letnie-serii/dlya-zagara",
        "https://apteka-ot-sklada.ru/catalog/tovary-dlya-mamy-i-malysha/butylochki/butylochki-s-rozhdeniya-_0-_",]

    def parse(self, response):
        products = response.css(".ui-card_outlined.goods-card.goods-grid__cell.goods-grid__cell_size_3")

        for product in products:
            yield {
                "timestamp": datetime.datetime.now(),
                "RPC": '',
                "title": product.css(".goods-card__name.text.text_size_default.text_weight_medium a span::text").get(),
                "url": 'https://apteka-ot-sklada.ru'+product.css(".text_weight_medium a").attrib['href'],
                "marketing_tags": product.css("li.goods-tags__item span::text").getall(),
                "brand": product.xpath("//div/div[1]/div[2]/div[2]/div/span[2]/text()").get(),
                "section": response.xpath("//main/header/div[1]/ul/li/a/span/span/text()").getall(),
                "price_data": {
                    "current": '',
                    "original":  product.css("a .ui-link__text span::text").get(),
                    "sale_tag": ''},
                "stock": {
                    "in_stock": product.css("a .ui-link__text span::text").get(),
                    "count": product.css(".goods-card__delivery-availability.text.text_weight_medium span::text").get(),
                    },
                "assets": {
                    "main_image": 'https://apteka-ot-sklada.ru'+[img.attrib["src"] for img in response.css("img")][2],
                    "set_images": [img.attrib["src"] for img in response.css("img")][2:5],
                    "view360": '',
                    "video": '',
                    },
                "metadata": {
                    "description": product.xpath('//*[@id="description"]/div/div[1]/div').get(),
                    "АРТИКУЛ": "",
                    "СТРАНА ПРОИЗВОДИТЕЛЬ": product.css(".goods-card__producer.text span::text").get(),
                    }
            }
            next_page = response.css(".ui-pagination__item_next a::attr(href)").get()

            if next_page is not None:
                if "/catalog/" in next_page:
                    next_page_url = "" + next_page
                else:
                    next_page_url = "https://apteka-ot-sklada.ru/catalog/" + next_page
                yield response.follow(next_page_url, callback=self.parse)
