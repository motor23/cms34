# -*- coding: utf-8 -*-
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property
from cms34.resources.menu.front import Menu

from ..front.environment import Environment as EnvironmentBase


class Context(EnvironmentBase.Context): pass


class Environment(EnvironmentBase):

    @cached_property
    def cached_db(self):
        return self.app.cached_db_maker()

    def get_template_vars(self):
        result = EnvironmentBase.get_template_vars(self)
        result['url_for_obj']=self.url_for_obj
        return result

    @storage_method
    def url_for_obj(storage, obj, default=None):
        if isinstance(obj, storage.models.Menu):
            return storage.menu.url_for_item(obj)
        elif isinstance(obj, storage.models.Block):
            return storage.url_for('index')
        url = storage.sections.url_for_obj(storage.lang.root, obj)
        return url and url or default

    @storage_cached_property
    def menu(storage):
        return Menu(storage, storage.models.Menu)

    @storage_cached_property
    def sections(storage):
        result = {}
        for key, section in storage.app.sections.items():
            cache = storage.cfg.QUERY_CACHE_ENABLED and storage.cache or None
            result[key] = section.bind(storage.db, cache)
        return result
