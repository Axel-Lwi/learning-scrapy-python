# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        #strip whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

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
            adapter('stock') = 0
        else:
            stock_array = split_string_array[1].split(' ')
            adapter('stock') = int(stock_array[0])

        ## review to number(int)
        reviews_string = adapter.get('reviews')
        reviews_array = reviews_string.split(' ')
        adapter('reviews') = int(reviews_array[0])

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

        return item