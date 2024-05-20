from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def handler(event, context):
    process = CrawlerProcess(get_project_settings())

    try:
        process.crawl('exchange_rate')
        process.start()

        return {
            'statusCode': 200,
            'body': '[INFO] Crawler function invoked'
        }
    except Exception as e:
        return {
            'statusCode': 422,
            'message': '[ERRO] Crawler function failed to proccess',
            'error': e
        }
