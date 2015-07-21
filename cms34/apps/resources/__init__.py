# -*- coding:utf8 -*-
from iktomi.web import Reverse
from iktomi.utils import cached_property
from cms34.resources import V_Sections
from ..common.cached_db import CachedDb
from ..front import Application as BaseApplication


class Application(BaseApplication):

    resources = []

    @property
    def root(self):\
        # XXX Is it is fast? 
        return Reverse.from_handler(self.handler)

    def cached_db_maker(self):
        if self.cfg.QUERY_CACHE_ENABLED is None:
            cache_enabled = self.cfg.CACHE_ENABLED
        else:
            cache_enabled = self.cfg.QUERY_CACHE_ENABLED
        return CachedDb(self.cache, cache_enabled=cache_enabled)

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import Environment
        return Environment

    def sections_maker(self, lang, db=None, cached_db=None):
        return V_Sections(
                   db = db or self.db_maker(),
                   cached_db = cached_db or self.cached_db_maker(),
                   model = getattr(self.front_models, lang).Section,
                   resources = self.resources,
        )

    class i18n_cls(BaseApplication.i18n_cls):
        def set_active_lang(self, env, active):
            BaseApplication.i18n_cls.set_active_lang(self, env, active)
            env.sections = env.app.sections_maker(active,
                                            db=env.db, cached_db=env.cached_db)

