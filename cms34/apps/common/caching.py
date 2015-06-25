# coding: utf-8
import logging
from hashlib import md5

import memcache
from iktomi.web import WebHandler, Response, request_filter


logger = logging.getLogger(__name__)


CACHE_ENABLE_ATTR = '__cache_enable'
CACHE_DURATION_ATTR = '__cache_duration'


def cache(enable=True, duration=None):
    @request_filter
    def handler(env, data, next_handler):
        response = next_handler(env, data)
        if response and not hasattr(response, CACHE_ENABLE_ATTR):
            setattr(response, CACHE_ENABLE_ATTR, enable)
            setattr(response, CACHE_DURATION_ATTR, duration)
        return response
    return handler


class EnhancedMemcachedBackend(object):

    def __init__(self, hash_keys_with_md5=True):
        self.hash_keys_with_md5 = hash_keys_with_md5

    def key(self, key):
        if self.hash_keys_with_md5:
            return md5(key).hexdigest()
        if len(key) > 250:
            return None
        return key

    def pack(self, headers, body):
        head = '\r\n'.join([': '.join(header) for header in headers.iteritems()])
        if head:
            head = '\r\n'.join(['EXTRACT_HEADERS', head])
        else:
            head = 'EXTRACT_HEADERS'
        return '\r\n\r\n'.join([head, body])

    def unpack(self, content):
        if content.startswith('EXTRACT_HEADERS\r\n'):
            head, body = content.split('\r\n\r\n')
            headers = head.split('\r\n')[1:]
            headers = dict([header.split(': ') for header in headers])
            return headers, body
        return {}, None

    def store(self, client, key, headers, body, time):
        key = self.key(key)
        if key is not None:
            content = self.pack(headers, body)
            client.set(key, content, time)
            logger.info('Store response to cache with key %s', key)
            return True
        return False

    def retrieve(self, client, key):
        key = self.key(key)
        content = client.get(key)
        if content is not None:
            logger.info('Retrieve response from cache by key %s', key)
            return self.unpack(content)
        return {}, None


class Caching(WebHandler):
    backend_cls = EnhancedMemcachedBackend

    def __init__(self, client, duration, content_type='text/html'):
        self.client = client
        self.duration = duration
        self.content_type = content_type
        self.backend = self.backend_cls()

    def __call__(self, env, data):
        if env.request.method in ['HEAD', 'GET']:
            return self.try_cache(env, data)
        return self.next_handler(env, data)

    def try_cache(self, env, data):
        response = self.retrieve_from_cache(env.request.url)
        if response is None:
            response = self.next_handler(env, data)
            if response and getattr(response, CACHE_ENABLE_ATTR, False):
                duration = getattr(response, CACHE_DURATION_ATTR, None) or self.duration
                self.store_to_cache(env.request.url, response, duration)
            else:
                logger.info('Cache skipped for %s', env.request.url)
        return response

    def retrieve_from_cache(self, key):
        headers, body = self.backend.retrieve(self.client, key)
        if body is None:
            return None
        return Response(body, headers=headers)

    def store_to_cache(self, key, response, duration):
        headers = dict(response.headerlist)
        body = response.body
        self.backend.store(self.client, key, headers, body, duration)


class MemcacheClient(object):

    def __init__(self, servers, prefix=''):
        self.client = memcache.Client(servers)
        self.prefix = prefix

    def get(self, key):
        return self.client.get(self.prefix + key)

    def set(self, key, value, time=0):
        return self.client.set(self.prefix + key, value, time)

    def add(self, key, value, time=0):
        return self.client.add(self.prefix + key, value, time)

    def delete(self, key, time=0):
        return self.client.delete(self.prefix + key)

    def cas(self, key, value, time=0):
        return self.client.cas(self.prefix + key, value, time)

    @property
    def cas_ids(self):
        return self.client.cas_ids

    def gets(self, key):
        return self.client.gets(self.prefix + key)
