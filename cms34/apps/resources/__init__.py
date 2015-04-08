# -*- coding:utf8 -*-
from iktomi.utils import cached_property
from cms34.resources import Resources

from ..common.cached_db import CachedDbMaker
from ..front import Application as BaseApplication


class Application(BaseApplication):

    resources = []

    @cached_property
    def resources_ru(self):
        from models.front import SectionRu
        return Resources(self, SectionRu, resources=self.resources)

    @cached_property
    def resources_en(self):
        from models.front import SectionEn
        return Resources(self, SectionEn, resources=self.resources)

    @cached_property
    def cached_db_maker(self):
        from models.front import SectionRu, SectionEn, MenuRu, MenuEn
        return CachedDbMaker(self.db_maker, self.cache,
                        preladed_models=[SectionRu, SectionEn, MenuRu, MenuEn],
                        cache_enabled=self.cfg.CACHE_ENABLED)

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import Environment
        return Environment

    class i18n_cls(BaseApplication.i18n_cls):
        def set_active_lang(self, env, active):
            BaseApplication.i18n_cls.set_active_lang(self, env, active)
            env.resources = getattr(env.app, 'resources_%s' % active)
