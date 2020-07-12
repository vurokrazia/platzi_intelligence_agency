import scrapy


class SpiderCIA(scrapy.Spider):

    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections']

    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 1024,
        'MEMUSAGE_NOTIFY_EMAIL': ['jesus.alberto.vk@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'VUROKRAZIA',
        'FEED_EXPORT_ENCODING': 'UTF-8'
    }

    def parse(self, response):
        links = '//a[starts-with(@href,"collection") and (parent::h3 | parent::h2)]/@href'
        title = '//h1[@class="documentFirstHeading"]/text()'
        paragraph = '//div[@class="field-item even"]//p[not(@class)]/text()'

        links_declassified = response.xpath(links).getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):

        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath(
            '//div[@class="field-item even"]//p[not(@class)]/text()').get()

        yield {
            'url':      link,
            'title':    title,
            'body':     paragraph
        }
