# -*- coding:utf8 -*-
from iktomi.web import Reverse
from iktomi.utils import cached_property
from cms34.resources import V_Sections
from ..common.cached_db import CachedDbMaker
from ..front import Application as BaseApplication


class Application(BaseApplication):

    resources = []

    @property
    def root(self):\
        # XXX Is it is fast? 
        return Reverse.from_handler(self.handler)

    @cached_property
    def cached_db_maker(self):
        return CachedDbMaker(self.db_maker, self.cache,
                             cache_enabled=self.cfg.CACHE_ENABLED,
                             db_limit=self.cfg.CACHE_DB_LIMIT)

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import Environment
        return Environment

    def sections_maker(self, lang):
        return V_Sections(
                   cached_db=self.cached_db_maker(),
                   model=getattr(self.front_models, lang).Section,
                   resources=self.resources,
        )

    class i18n_cls(BaseApplication.i18n_cls):
        def set_active_lang(self, env, active):
            BaseApplication.i18n_cls.set_active_lang(self, env, active)
            env.sections = env._sections[active]

