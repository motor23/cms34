# -*- coding: utf-8 -*-

import logging

from cms34.utils import cached_property
from iktomi.utils.storage import VersionedStorage
from iktomi.web import (
    Application as BaseApplication,
    Reverse,
)
from webob import Request
from webob.exc import (
    HTTPException,
    HTTPInternalServerError,
    HTTPNotFound,
)
from .caching import MemcacheClient
from .cli import AppCliDict, AppCli
from .templates import AppTemplateEngine

__all__ = ['Application', 'AppEnvironment']
logger = logging.getLogger()


class BaseApplication(object):

    properties = [
        'env_class',
        'handler',
        'root',
    ]

    cli_dict = AppCliDict([AppCli])

    def __init__(self, cfg=None, **kwargs):
        self.cfg = cfg or self.cfg_class()()
        self.__dict__.update(kwargs)
        for name in self.properties:
            if name not in kwargs and name not in dir(self):
                logging.debug('Application: load "%s" property' % name)
                setattr(self, name, getattr(self, 'get_%s' % name)())

    @classmethod
    def custom(cls, custom_cfg_path='', **kwargs):
        cfg_cls = cls.cfg_class()
        cfg = cfg_cls(**kwargs)
        # Apply default local config (if any) to app, then apply custom config.
        cfg.update_from_py(cfg.DEFAULT_CUSTOM_CFG)
        # Kwargs has more priority then default cfg values,
        # so we need to update then once more.
        # But `update_cfg` do not correctly update properties, be careful.
        cfg.update_cfg(kwargs)
        cfg.update_from_py(custom_cfg_path)
        return cls(cfg)

    @classmethod
    def cfg_class(cls):
        from .cfg import Cfg
        return Cfg

    def get_handler(self):
        raise NotImplementedError()

    def get_root(self):
        host = self.cfg.DOMAINS[0] if self.cfg.DOMAINS else ''
        return Reverse(self.handler._locations(), host=host)

    def get_env_class(self):
        from .environment import Environment
        return Environment

    def create_environment(self, request=None, **kwargs):
        return self.env_class.create(self, request=request, **kwargs)

    def create_request(self, environ):
        return Request(environ, charset='utf-8')

    def handle_error(self, env):
        '''
        Unhandled exception handler.
        You can put any logging, error warning, etc here.'''
        logger.exception('Exception for %s %s :',
                         env.request.method, env.request.url)

    def handle(self, env, data):
        '''
        Calls application and handles following cases:
            * catches `webob.HTTPException` errors.
            * catches unhandled exceptions, calls `handle_error` method
              and returns 500.
            * returns 404 if the app has returned None`.
        '''
        try:
            try:
                response = self.handler(env, data)
            finally:
                env.finalize()
            if response is None:
                logger.debug('Application returned None '
                             'instead of Response object')
                response = HTTPNotFound()
        except HTTPException, e:
            response = e
        except Exception, e:
            self.handle_error(env)
            response = HTTPInternalServerError()
        return response

    def __call__(self, environ, start_response):
        '''
        WSGI interface method.
        Creates webob and iktomi wrappers and calls `handle` method.
        '''
        request = self.create_request(environ)
        env = self.create_environment(request)
        data = VersionedStorage()
        response = self.handle(env, data)
        try:
            result = response(environ, start_response)
        except Exception:
            self.handle_error(env)
            result = HTTPInternalServerError()(environ, start_response)
        return result


class Application(BaseApplication):

    properties = [
        'template_engine',
        'db_maker',
        'cache',
        'models',
        'env_class',
        'handler',
        'root',
    ]

    def get_db_maker(self):
        return binded_filesessionmaker(self.cfg.DATABASES,
                                       engine_params=self.cfg.DATABASE_PARAMS,
                                       )

    def get_cache(self):
        return MemcacheClient(self.cfg.MEMCACHE, self.cfg.CACHE_PREFIX)

    def get_template_engine(self):
        return AppTemplateEngine(self, self.cfg.TEMPLATES)

    def get_models(self):
        import models
        return models

