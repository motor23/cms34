# -*- coding:utf8 -*-
import json

from webob.exc import HTTPSeeOther
from jinja2 import Markup
from iktomi.templates import BoundTemplate as BaseBoundTemplate
from iktomi import web
from iktomi.utils import cached_property, quote_js
from iktomi.utils.storage import (
    StorageFrame,
    storage_cached_property,
    storage_method,
    storage_property,)

from iktomi.web.route_state import RouteState
import models


class BoundTemplate(BaseBoundTemplate):

    constant_template_vars = {
        'quote_js': quote_js,
    }

    def get_template_vars(self):
        d = dict(
            self.constant_template_vars,
            env = self.env,
            url_for = self.env.url_for,
            url_for_static = self.env.url_for_static,
            context = self.env.context,
        )
        return d

    def render(self, template_name, __data=None, **kw):
        r = BaseBoundTemplate.render(self, template_name, __data, **kw)
        return Markup(r)


class Context(object):
    def __init__(self, env):
        self.env = env


class BaseEnvironment(web.AppEnvironment):

    def __init__(self, app, request=None, **kwargs):
        StorageFrame.__init__(self, **kwargs)
        self.app = app
        self.cfg = app.cfg
        self.request = request
        self._route_state = RouteState(request)

    @cached_property
    def root(self):
        if self.request:
            return self.app.root.bind_to_env(self._root_storage)
        else:
            return self.app.root

    def finalize(self):
        pass


class Environment(BaseEnvironment):
    models = models
    BoundTemplate = BoundTemplate
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
        try:
            return storage.BoundTemplate(storage, storage.app.template_loader)
        except Exception, err:
            raise Exception(err)

    @storage_property
    def render_to_string(storage):
        return storage.template.render

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


