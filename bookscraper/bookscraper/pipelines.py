# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2


class BookscraperPipeline:
    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres' # your password
        database = 'scrapy'

    ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
    ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

    ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS scrapy(
            id serial PRIMARY KEY, 
            url text,
            title text,
            price float,
            product_type text,
            stock int,
            rating int,
            category text,
            reviews int,
            description text
        )
        """)    

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #strip whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        ##turn fields into lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ##turn price into float
        price_keys = ['price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## availbility to int
        stock_string = adapter.get('stock')
        split_string_array = stock_string.split('(')
        if len(split_string_array) > 2:
            adapter['stock'] = 0
        else:
            stock_array = split_string_array[1].split(' ')
            adapter['stock'] = int(stock_array[0])

        ## review to number(int)
        reviews_string = adapter.get('reviews')
        reviews_array = reviews_string.split(' ')
        adapter['reviews'] = int(reviews_array[0])

        ## rating to number int
        rating_string = adapter.get('rating')
        split_rating_array = rating_string.split(' ')
        rating_text_value = split_rating_array[1].lower()
        if rating_text_value == 'zero':
            adapter['rating'] = 0
        elif rating_text_value == 'one':
            adapter['rating'] = 1
        elif rating_text_value == 'two':
            adapter['rating'] = 2
        elif rating_text_value == 'three':
            adapter['rating'] = 3
        elif rating_text_value == 'four':
            adapter['rating'] = 4
        elif rating_text_value == 'five':
            adapter['rating'] = 5
    
        
        ## Define insert statement
        self.cur.execute(""" insert into scrapy (url, title, price, product_type, stock, rating, category, reviews, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get("url", None),
            item.get("title", None),
            item.get("price", None),
            item.get("product_type", None),
            item.get("stock", None),
            item.get("rating", None),
            item.get("category", None),
            item.get("reviews", None),
            item.get("description", None)
        ))

        ## Execute insert of data into database
        self.connection.commit()

        return item
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()