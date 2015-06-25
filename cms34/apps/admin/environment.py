# -*- coding: utf-8 -*-
#import inspect

from functools import partial
from jinja2 import Markup

from iktomi.cms.views import AdminAuth
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property
from iktomi.cms.item_lock import ItemLock

import models

from ..common.environment import Environment as EnvironmentBase

from .views import packer


class Context(EnvironmentBase.Context):

    import json

    @cached_property
    def top_menu(self):
        return self.env.top_menu(self.env)

    @cached_property
    def users(self):
        return self.env.db.query(AdminUser).filter_by(active=True).all()

    def preview_buttons(self, item, buttons=['edit']):
        result = {}
        result['data-preview'] = 'bottom'
        for button in buttons:
            if button=='edit':
                result['data-preview-edit'] = self.env.url_for_obj(item)
        result = ['%s="%s"' % (key, value) for key, value in result.items()]
        return Markup(' '.join(result))

    def preview_panel(self):
        return Markup(self.env.render_to_string('preview_panel'))


class Environment(EnvironmentBase):
    Context = Context
    auth_model = models.admin.AdminUser
    object_tray_model = models.admin.ObjectTray #XXX tmp huck

    def __init__(self, app, **kwargs):
        EnvironmentBase.__init__(self, app, **kwargs)
        self.streams = app.streams
        self.dashboard = app.dashboard
        self.top_menu = app.top_menu

    @storage_cached_property
    def item_lock(storage):
        return ItemLock(storage)

    @storage_method
    def get_edit_url(storage, x):
        return streams.get_edit_url(storage, x)

    def get_template_globals(self, env):
        vars = EnvironmentBase.get_template_globals(self, env)
        vars.update(dict(
            user = getattr(env, 'user', None),
            packed_js_tag = partial(packer.js_tag, env),
            packed_css_tag = partial(packer.css_tag, env),
            CMS34_STATIC_URL = env.cfg.CMS34_STATIC_URL,
            CMS_STATIC_URL = env.cfg.CMS_STATIC_URL,
        ))
        return vars

    @storage_method
    def root_for_stream(storage, stream):
        return storage.root.build_subreverse(stream.module_name,
                                             lang=storage.lang)

    @storage_method
    def url_for_obj(storage, obj, name='item', **kwargs):
        streams = filter(lambda x: getattr(x.config, 'obj_endpoint', None), \
                         storage.streams.values())
        for stream in streams:
            model = stream.get_model(storage)
            if isinstance(obj, model):
                return stream.url_for(storage, name, item=obj.id, **kwargs)
        else:
            raise Exception('Add url_for_model to stream')
