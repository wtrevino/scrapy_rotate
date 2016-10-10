from fake_useragent import UserAgent as FakeUserAgent
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
        default_useragent = spider.settings.get('USER_AGENT', None)
        if callable(default_useragent):
            default_useragent = default_useragent()
        self.default_useragent = default_useragent

    def process_request(self, request, spider):
        if self.use_default_useragent:
            request.headers['User-Agent'] = self.default_useragent
            return

        request.headers['User-Agent'] = self.get_useragent_string()


class RotateFakeUserAgentMiddleware(RotateUserAgentMiddleware):

    def spider_opened(self, spider):
        super(RotateFakeUserAgentMiddleware, self).spider_opened(spider)
        if not self.use_default_useragent:
            self.fake_useragent = FakeUserAgent()
            self.rotate_browsers = spider.settings.getlist('ROTATE_BROWSER_CHOICES')

    def get_useragent_string(self):
        choice = random.choice(self.rotate_browsers) if self.rotate_browsers else 'random'
        return self.fake_useragent[choice]


class RotateFileUserAgentMiddleware(RotateUserAgentMiddleware):

    def spider_opened(self, spider):
        super(RotateFileUserAgentMiddleware, self).spider_opened(spider)
        useragent_file = settings.get('ROTATE_USERAGENT_FILE')
        with open(useragent_file, 'r') as f:
            from ipdb import set_trace;set_trace()
            self.user_agent_list = [line.strip() for line in f.readlines() if line]
            self.user_agent_list = list(set(self.user_agent_list))

    def get_useragent_string(self):
        return random.choice(self.user_agent_list)


class RotateProxyMiddleware(object):
    pass
