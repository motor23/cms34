# -*- coding:utf8 -*-
from iktomi.utils import cached_property

from ..common.cached_db import CachedDbMaker
from ..front import Application as BaseApplication


class Application(BaseApplication):

    @cached_property
    def resources(self):
        from .resources import Resources
        return Resources(self, resources=[
        ])

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

