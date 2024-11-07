# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def seriealize_price(value):
    # good for low effort data scraping without using pipeline
    return f'£ {str(value)}'

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field(serializer = seriealize_price)
    product_type = scrapy.Field()
    stock = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    reviews = scrapy.Field()
    description = scrapy.Field()
    
