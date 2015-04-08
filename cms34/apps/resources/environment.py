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

    @storage_method
    def url_for_obj(storage, obj):
        url = storage.resources.url_for_section(storage.lang.root, obj)
        if url:
            return url

    @storage_cached_property
    def menu(storage):
        return Menu(storage, storage.models.Menu)
