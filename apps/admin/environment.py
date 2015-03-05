# -*- coding: utf-8 -*-
#import inspect

from functools import partial

from iktomi.cms.views import AdminAuth
from iktomi import web
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property
from iktomi.cms.item_lock import ItemLock

import models

from ..common.environment import Environment

from .views import packer


class BoundTemplate(Environment.BoundTemplate):

    def get_template_vars(self):
        d = Environment.BoundTemplate.get_template_vars(self)
        d.update(dict(
            user = getattr(self.env, 'user', None),
            packed_js_tag = partial(packer.js_tag, self.env),
            packed_css_tag = partial(packer.css_tag, self.env),
            STATIC_URL = self.env.cfg.STATIC_URL,
            CMS_STATIC_URL = self.env.cfg.CMS_STATIC_URL,
        ))
        return d


class Context(Environment.Context):

    import json

    @cached_property
    def top_menu(self):
        return self.env.top_menu(self.env)

    @cached_property
    def users(self):
        return self.env.db.query(AdminUser).filter_by(active=True).all()


class AdminEnvironment(Environment):
    Context = Context
    BoundTemplate = BoundTemplate

    def __init__(self, app, **kwargs):
        Environment.__init__(self, app, **kwargs)
        self.streams = app.streams
        self.dashboard = app.dashboard
        self.top_menu = app.top_menu


    @cached_property
    def url_for_static(self):
        return web.filters.static_files('admin/static').construct_reverse()

    @storage_cached_property
    def item_lock(storage):
        return ItemLock(storage)

    @storage_method
    def get_edit_url(storage, x):
        return streams.get_edit_url(storage, x)

 
