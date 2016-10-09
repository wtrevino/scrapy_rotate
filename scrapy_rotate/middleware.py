from fake_useragent import UserAgent
from scrapy.signals import spider_opened

import random



class RotateUserAgentMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=spider_opened)
        return o

    def spider_opened(self, spider):
        self.fake_ua = UserAgent()

    def process_request(self, request, spider):
        keep_original_ua = getattr(spider, 'keep_original_ua', False)
        if keep_original_ua:
            request.headers['User-Agent'] = spider.settings.get('USER_AGENT', 'Scrapy')

        else:
            rotate_browsers = spider.settings.getlist('ROTATE_BROWSER_CHOICES')
            user_agent = random.choice(rotate_browsers) if rotate_browsers else 'random'
            request.headers['User-Agent'] = self.fake_ua[user_agent]


class RotateProxyMiddleware(object):
    pass
