import scrapy
from src.utils import *


class ExchangeRateSpider(scrapy.Spider):
    name = "exchange_rate"
    allowed_domains = ["kursdollar.org"]
    start_urls = ["https://kursdollar.org/bank/mandiri.php"]

    def parse(self, response, **kwargs):
        for rates in response.css('table'):
            # bank_notes = rate.xpath("//tr[@class='title_table'][1]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 3]").getall()
            # dd_tt = rate.xpath("//tr[@class='title_table'][3]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 5]").getall()
            # e_rates = rate.xpath("//tr[@class='title_table'][5]/following-sibling::tr").getall()

            bank_notes = rates.xpath("//tr[@class='title_table'][1]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 2]").getall()
            dd_tt = rates.xpath("//tr[@class='title_table'][2]/following-sibling::tr[count(preceding-sibling::tr[@class='title_table']) < 3]").getall()
            e_rates = rates.xpath("//tr[@class='title_table'][3]/following-sibling::tr").getall()

            tables = {
                'bank_notes': bank_notes,
                'dd_tt': dd_tt,
                'e_rates': e_rates
            }

            yield scrapy.Request(
                response.url,
                callback=self.parse_bank_notes_buy_rates,
                meta=tables
            )

    def parse_bank_notes_buy_rates(self, response):
        date_field = ''
        idr_exchange_rate = {
            "USD": {},
        }

        for i, rate in enumerate(response.meta['bank_notes']):
            element_selector = scrapy.Selector(text=rate)
            if i % 2 == 0:
                ## date always in even row
                date_field = element_selector.css('td:nth-child(1)::text').getall()

                ## record beli
                idr_exchange_rate['USD']['buy'] = element_selector.css('td:nth-child(3)::text').get() or ''
                # sgd = scrapy.Selector(text=rate).css('td:nth-child(4)::text').get()

                ## skip adding to yield to make sure buy & sell tied together in one record
                continue
            else:
                ## record jual
                idr_exchange_rate['USD']['sell'] = element_selector.css('td:nth-child(2)::text').get() or ''
                # sgd = scrapy.Selector(text=rate).css('td:nth-child(3)::text').get()

                ## skip if there's no data
                if not (date_field and idr_exchange_rate['USD']['buy']):
                    continue

            yield {
                'type': 'bank notes',
                'url': response.url,
                'bank': parse_bank_name(response.url),
                'date': ' '.join(date_field),
                'IDRExchangeRate': idr_exchange_rate,
            }
