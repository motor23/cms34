# -*- coding: utf-8 -*-

__all__ = ['Application', 'AppEnvironment']

from webob.exc import HTTPException, HTTPInternalServerError, \
                      HTTPNotFound
from webob import Request
import memcache
from .templates import AppTemplateEngine
from iktomi.utils import cached_property
from iktomi.utils.storage import VersionedStorage
from iktomi.web import (
    Application as BaseApplication,
    Reverse,
)
from iktomi.cli.base import Cli


class DeferredCommand(Cli):

    def __init__(self, func):
        self.get_digest = func

    @cached_property
    def digest(self):
        return self.get_digest()

    def description(self, *args, **kwargs):
        return self.digest.description(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.digest(*args, **kwargs)


class Application(BaseApplication):

    def __init__(self, cfg, **kwargs):
        self.cfg = cfg
        self.__dict__.update(kwargs)

    @cached_property
    def handler(self):
        raise NotImplementedError()

    @cached_property
    def root(self):
        return Reverse.from_handler(self.handler)

    @cached_property
    def env_class(self):
        from .environment import BaseEnvironment
        return BaseEnvironment

    def create_environment(self, request=None):
        return self.env_class.create(self, request=request)

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
    def commands(self):
        commands = {}
        for name in dir(self):
            if name.startswith('command_'):
                commands[name[8:]] = DeferredCommand(getattr(self, name))
        return commands

    @cached_property
    def db_maker(self):
        return binded_filesessionmaker(self.cfg.DATABASES,
                                   engine_params=self.cfg.DATABASE_PARAMS,
                                   )

    @cached_property
    def cache(self):
        return memcache.Client(self.cfg.MEMCACHE)


    def template_engine(self):
        return AppTemplateEngine(self.cfg.TEMPLATES)

    @cached_property
    def models(self):
        import models
        return models

