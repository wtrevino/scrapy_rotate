from unittest import TestCase

from scrapy.spiders import Spider
from scrapy.http import Request, Response, HtmlResponse
from scrapy.utils.test import get_crawler
from scrapy.settings import Settings

from scrapy_rotate.middleware import RotateFakeUserAgentMiddleware
import os


class RotateTestCaseMixin(object):

    def _setup_crawler(self, req_kwargs={}):
        self.crawler = get_crawler(Spider, req_kwargs)
        self.spider = self.crawler._create_spider('foo')
        self.mw = RotateFakeUserAgentMiddleware.from_crawler(self.crawler)
        self.mw.spider_opened(self.spider)

    def _req_resp(self, url, req_kwargs=None, resp_kwargs=None):
        req = Request(url, **(req_kwargs or {}))
        resp = HtmlResponse(url, request=req, **(resp_kwargs or {}))
        return req, resp

    def _process_request_response(self, req, resp):
        req2 = self.mw.process_request(req, self.spider)
        resp2 = self.mw.process_response(req, resp, self.spider)
        return req2, resp2


class RotateFakeUserAgentMiddlewareTestCase(RotateTestCaseMixin, TestCase):

    def test_fake_useragent(self):
        '''
            Check that the useragent string matches
            the one in the request headers.
        '''
        self._setup_crawler({})
        req, resp = self._req_resp('http://example.com/', {'method': 'GET'})
        req2, resp2 = self._process_request_response(req, resp)
        headers_useragent = req.headers['User-Agent'].decode('utf8')
        self.assertEqual(self.mw.useragent, headers_useragent)

    def test_fake_useragent_choices(self):
        '''
            Check that the useragent string belongs
            to the right browser, given provided choices
        '''
        self._setup_crawler({'ROTATE_BROWSER_CHOICES': ['opera']})
        req, resp = self._req_resp('http://example.com/', {'method': 'GET'})
        req2, resp2 = self._process_request_response(req, resp)
        headers_useragent = req.headers['User-Agent'].decode('utf8')
        self.assertEqual('Opera' in self.mw.useragent, True)

        self._setup_crawler({'ROTATE_BROWSER_CHOICES': ['msie']})
        req, resp = self._req_resp('http://example.com/', {'method': 'GET'})
        req2, resp2 = self._process_request_response(req, resp)
        headers_useragent = req.headers['User-Agent'].decode('utf8')
        self.assertEqual('Windows NT' in self.mw.useragent, True)
