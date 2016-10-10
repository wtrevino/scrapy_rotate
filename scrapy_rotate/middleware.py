from fake_useragent import UserAgent as FakeUserAgent
from scrapy.signals import spider_opened

import random
import base64


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

    def get_useragent_string(self):
        raise NotImplementedError

    def process_request(self, request, spider):
        if self.use_default_useragent:
            request.headers['User-Agent'] = self.default_useragent
            return

        request.headers['User-Agent'] = self.get_useragent_string()


class RotateFakeUserAgentMiddleware(RotateUserAgentMiddleware):

    def spider_opened(self, spider):
        super(RotateFakeUserAgentMiddleware, self).spider_opened(spider)
        if not self.use_default_useragent:
            cache = spider.settings.get('ROTATE_FAKE_USERAGENT_CACHE', True)
            self.fake_useragent = FakeUserAgent(cache=cache)
            self.rotate_browsers = spider.settings.getlist('ROTATE_BROWSER_CHOICES')

    def get_useragent_string(self):
        choice = random.choice(self.rotate_browsers) if self.rotate_browsers else 'random'
        return self.fake_useragent[choice]


class RotateFileUserAgentMiddleware(RotateUserAgentMiddleware):

    def spider_opened(self, spider):
        super(RotateFileUserAgentMiddleware, self).spider_opened(spider)
        useragent_file = spider.settings.get('ROTATE_USERAGENT_FILE')  # TODO: raise error when None
        with open(useragent_file, 'r') as f:
            self.user_agent_list = [line.strip() for line in f.readlines() if line.strip()]
            self.user_agent_list = list(set(self.user_agent_list))

    def get_useragent_string(self):
        return random.choice(self.user_agent_list)


class RotateProxyMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=spider_opened)
        return o

    def spider_opened(self, spider):
        proxy_list = spider.settings.getlist('ROTATE_PROXY_LIST')
        proxy_auth = spider.settings.get('ROTATE_PROXY_AUTH', '')
        self.proxy_dict = {'{}'.format(proxy): proxy_auth for proxy in proxy_list}

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            return

        proxy_list = list(self.proxy_dict.keys())
        proxy = random.choice(proxy_list)
        auth = self.proxy_dict[proxy]

        request.meta['proxy'] = proxy
        if auth:  # TODO: check this actually works...
            basic_auth = 'Basic ' + base64.encodestring(auth)
            request.headers['Proxy-Authorization'] = basic_auth

    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta:
            proxy = request.meta['proxy']
            try:
                del self.proxy_dict[proxy]
            except KeyError:
                pass
