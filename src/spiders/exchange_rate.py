import scrapy


class ExchangeRateSpider(scrapy.Spider):
    banks = ['bi', 'bca', 'bni', 'bri', 'mandiri', 'ekonomi', 'permata', 'ocbc', 'btn', 'panin']
    query = 'v_range=01/01/2024-05/31/2024'

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

            yield {
                "tables": tables
            }
