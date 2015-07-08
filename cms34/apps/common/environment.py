# -*- coding:utf8 -*-
import os, json

from webob.exc import HTTPSeeOther
from jinja2 import Markup
from iktomi.templates import BoundTemplate
from iktomi import web
from iktomi.utils import cached_property, quote_js
from iktomi.utils.storage import (
    StorageFrame,
    storage_cached_property,
    storage_method,
    storage_property,)

from iktomi.web.route_state import RouteState
import models


class Context(object):
    def __init__(self, env):
        self.env = env


class BaseEnvironment(web.AppEnvironment):

    def __init__(self, app, request=None, route_state=None, **kwargs):
        StorageFrame.__init__(self, **kwargs)
        self.app = app
        self.cfg = app.cfg
        self.request = request
        if route_state:
            self._route_state = route_state
        elif request:
            self._route_state = RouteState(request)

    @cached_property
    def root(self):
        try:
            if self.request:
                return self.app.root.bind_to_env(self._root_storage)
            else:
                return self.app.root
        except Exception, exc:
            import traceback
            traceback.print_exc()
            raise Exception(exc)

    def finalize(self):
        pass

    @storage_cached_property
    def url_for(self):
        raise Exception()
        return self.root.build_url

    def url_for_static(self, path):
        if self.cfg.DEV_STATIC:
            return self.cfg.DEV_STATIC_URL + path
        else:
            return self.cfg.STATIC_URL + path


class Environment(BaseEnvironment):
    models = models
    Context = Context

    def __init__(self, app, **kwargs):
        self.cfg = app.cfg
        BaseEnvironment.__init__(self, app, **kwargs)

    @cached_property
    def db(self):
        return self.app.db_maker()

    @cached_property
    def cache(self):
        return self.app.cache

    @cached_property
    def url_for(self):
        return self.root.build_url

    @storage_cached_property
    def template(storage):
        import traceback
        template = storage.app.template_engine()
        try:
            template.env.globals.update(storage.get_template_globals(storage))
        except Exception, exc:
            traceback.print_exc(100)
            raise Exception(exc)
        return template

    def get_template_globals(self, env):
        return dict(
            env = env,
            url_for = self.url_for,
            url_for_static = self.url_for_static,
            context = self.context,
        )

    @storage_property
    def render_to_string(storage):
        return storage.template.render_to_string

    @storage_property
    def render_to_response(storage):
        return storage.template.render_to_response

    def json(self, data):
        return web.Response(json.dumps(data), content_type="application/json")

    @storage_method
    def redirect_to(storage, name, qs, **kwargs):
        url = storage.url_for(name, **kwargs)
        if qs:
            url = url.qs_set(qs)
        return HTTPSeeOther(location=str(url))

    @storage_cached_property
    def context(storage):
        return storage.Context(storage)

    def finalize(self):
        self.db.close()


