# -*- coding: utf-8 -*-

__all__ = ['Application', 'AppEnvironment']

import logging

from webob.exc import HTTPException, HTTPInternalServerError, \
                      HTTPNotFound
from webob import Request
import memcache
from .templates import AppTemplateEngine
from iktomi.utils.storage import VersionedStorage
from iktomi.web import (
    Application as BaseApplication,
    Reverse,
)

from cms34.utils import cached_property
from .cli import AppCliDict, AppCli
from .caching import MemcacheClient


logger = logging.getLogger()


class Application(BaseApplication):

    cli_dict = AppCliDict([AppCli])

    def __init__(self, cfg=None, **kwargs):
        self.cfg = cfg or self.cfg_class()()
        self.__dict__.update(kwargs)

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

    @cached_property
    def handler(self):
        raise NotImplementedError()

    @property
    def root(self):
        return Reverse.from_handler(self.handler)

    @cached_property
    def env_class(self):
        from .environment import BaseEnvironment
        return BaseEnvironment

    def create_environment(self, request=None, **kwargs):
        return self.env_class.create(self, request=request, **kwargs)

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
        request = Request(environ, charset='utf-8')
        env = self.create_environment(request)
        data = VersionedStorage()
        response = self.handle(env, data)
        try:
            result = response(environ, start_response)
        except Exception:
            self.handle_error(env)
            result = HTTPInternalServerError()(environ, start_response)
        return result

    @cached_property
    def db_maker(self):
        return binded_filesessionmaker(self.cfg.DATABASES,
                                   engine_params=self.cfg.DATABASE_PARAMS,
                                   )

    @cached_property
    def cache(self):
        return MemcacheClient(self.cfg.MEMCACHE, self.cfg.CACHE_PREFIX)


    def template_engine(self):
        return AppTemplateEngine(self.cfg.TEMPLATES)

    @cached_property
    def models(self):
        import models
        return models
