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
        self.use_default_useragent = getattr(spider, 'use_default_useragent', False)

        if not self.use_default_useragent:
            self.fake_ua = UserAgent()

    def process_request(self, request, spider):
        use_default_useragent = getattr(spider, 'use_default_useragent', False)
        if use_default_useragent:
            request.headers['User-Agent'] = spider.settings.get('USER_AGENT', None)
            return

        rotate_browsers = spider.settings.getlist('ROTATE_BROWSER_CHOICES')
        user_agent = random.choice(rotate_browsers) if rotate_browsers else 'random'
        request.headers['User-Agent'] = self.fake_ua[user_agent]


class RotateProxyMiddleware(object):
    pass
