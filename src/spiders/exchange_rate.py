import scrapy
from src.utils import *


base_url = "https://kursdollar.org/bank"
banks = ['bi', 'bca', 'bni', 'bri', 'mandiri', 'cimb', 'ekonomi', 'permata', 'ocbc', 'panin']
query = 'v_range=01/01/2024-05/31/2024'

class ExchangeRateSpider(scrapy.Spider):
    name = "exchange_rate"
    allowed_domains = ["kursdollar.org"]
    # start_urls = [f"{base_url}/{bank}.php" for bank in banks]
    start_urls = [f"{base_url}/{bank}.php?{query}" for bank in banks]

    def parse(self, response, **kwargs):
        for rates in response.css('table'):
            # bank_notes = rate.xpath("//tr[@class='title_table'][1]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 3]").getall()
            # dd_tt = rate.xpath("//tr[@class='title_table'][3]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 5]").getall()
            # e_rates = rate.xpath("//tr[@class='title_table'][5]/following-sibling::tr").getall()

            bank_notes = rates.xpath("//tr[@class='title_table'][1]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 2]").getall()
            dd_tt = rates.xpath("//tr[@class='title_table'][2]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 3]").getall()
            e_rates = rates.xpath("//tr[@class='title_table'][3]/following-sibling::tr").getall()

            bank_rates = {
                'tables': [
                    {'name': 'bank notes', 'payload': bank_notes},
                    {'name': 'dd/tt', 'payload': dd_tt},
                    {'name': 'e-rates', 'payload': e_rates},
                ]
            }

            yield scrapy.Request(
                response.url,
                callback=self.parse_bank_notes_buy_rates,
                meta=bank_rates
            )

    def parse_bank_notes_buy_rates(self, response):
        date_field = ''
        idr_exchange_rate = {
            "USD": {},
            "SGD": {},
            "EUR": {},
            "CNY": {},
            "GBP": {},
            "JPY": {},
            "SAR": {}
        }

        # loop bank rate tables
        for table in response.meta['tables']:

            # loop rows each table rates
            for i, rate in enumerate(table['payload']):
                element_selector = scrapy.Selector(text=rate)
                if i % 2 == 0:
                    ## date always in even row
                    date_field = element_selector.css('td:nth-child(1)::text').getall()

                    ## record beli
                    idr_exchange_rate['USD']['buy'] = parse_price_rate(element_selector.css('td:nth-child(3)::text').get())
                    idr_exchange_rate['SGD']['buy'] = parse_price_rate(element_selector.css('td:nth-child(4)::text').get())
                    idr_exchange_rate['EUR']['buy'] = parse_price_rate(element_selector.css('td:nth-child(6)::text').get())
                    # yuan is possibly null
                    idr_exchange_rate['CNY']['buy'] = parse_price_rate(element_selector.css('td:nth-child(7)::text').get(default=None))
                    idr_exchange_rate['GBP']['buy'] = parse_price_rate(element_selector.css('td:nth-child(9)::text').get())
                    idr_exchange_rate['JPY']['buy'] = parse_price_rate(element_selector.css('td:nth-child(10)::text').get())
                    # handling field for riyal
                    if parse_bank_name(response.url) == 'bi' or 'mandiri' or 'bca' or 'bni' or 'bri' or 'cimb':
                        idr_exchange_rate['SAR']['buy'] = parse_price_rate(element_selector.css('td:nth-child(15)::text').get())
                    elif parse_bank_name(response.url) == 'btn':
                        idr_exchange_rate['SAR']['buy'] = parse_price_rate(element_selector.css('td:nth-child(12)::text').get())
                    else:
                        idr_exchange_rate['SAR']['buy'] = None

                    ## skip adding to yield to make sure buy & sell tied together in one record
                    continue
                else:
                    ## record jual
                    idr_exchange_rate['USD']['sell'] = parse_price_rate(element_selector.css('td:nth-child(2)::text').get())
                    idr_exchange_rate['SGD']['sell'] = parse_price_rate(element_selector.css('td:nth-child(3)::text').get())
                    idr_exchange_rate['EUR']['sell'] = parse_price_rate(element_selector.css('td:nth-child(5)::text').get())
                    # yuan is possibly null
                    idr_exchange_rate['CNY']['sell'] = parse_price_rate(element_selector.css('td:nth-child(6)::text').get(default=None))
                    idr_exchange_rate['GBP']['sell'] = parse_price_rate(element_selector.css('td:nth-child(8)::text').get())
                    idr_exchange_rate['JPY']['sell'] = parse_price_rate(element_selector.css('td:nth-child(9)::text').get())
                    # handling field for riyal
                    if parse_bank_name(response.url) == 'bi' or 'mandiri' or 'bca' or 'bni' or 'bri':
                        idr_exchange_rate['SAR']['sell'] = parse_price_rate(element_selector.css('td:nth-child(14)::text').get())
                    elif parse_bank_name(response.url) == 'btn':
                        idr_exchange_rate['SAR']['sell'] = parse_price_rate(element_selector.css('td:nth-child(11)::text').get())
                    else:
                        idr_exchange_rate['SAR']['sell'] = None

                    ## skip if there's no data
                    if not (date_field and idr_exchange_rate['USD']['buy']):
                        continue

                yield {
                    'type': 'special rates' if (parse_bank_name(response.url) == 'mandiri' and table['name'] == 'e-rates') else table['name'],
                    'bank': parse_bank_name(response.url),
                    'date': parse_date_time(' '.join(date_field)),
                    'IDRExchangeRate': idr_exchange_rate,
                }
