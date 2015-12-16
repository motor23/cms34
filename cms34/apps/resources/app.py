# -*- coding:utf8 -*-
from iktomi.web import Reverse
from iktomi.utils import cached_property
from cms34.resources import V_Sections
from ..common.cached_db import CachedDb
from ..front import Application as BaseApplication


class Application(BaseApplication):

    properties = [
        'resources',
        'template_engine',
        'cache',
        'models',
        'front_models',
        'shared_models',
        'flood_models',
        'query_class',
        'front_file_manager',
        'shared_file_manager',
        'db_maker',
        'i18n',
        'resources',
        'sections',
        'env_class',
        'handler',
        'root',
    ]

    def get_resources(self):
        raise NotImplementedError

    def cached_db_maker(self):
        return CachedDb(self.cache, cache_enabled=self.cfg.QUERY_CACHE_ENABLED)

    def get_handler(self):
        from .handler import create_handler
        return create_handler(self)

    def get_env_class(self):
        from .environment import Environment
        return Environment

    def sections_maker(self, lang):
        return V_Sections(
                   model = getattr(self.front_models, lang).Section,
                   resources = self.resources,
        )

    def get_sections(self):
        result = {}
        for lang in ['ru', 'en']:
            result[lang] = self.sections_maker(lang)
        self.update_sections(result.values())
        return result

    def update_sections(self, sections_list):
        db = self.db_maker()
        result = False
        try:
            for sections in sections_list:
                cache = self.cfg.QUERY_CACHE_ENABLED and self.cache
                result = sections.bind(db, cache).update() or result
        finally:
            db.close()
        return result

    def create_environment(self, request=None, **kwargs):
        if self.update_sections(self.sections.values()):
            self.handler = self.get_handler()
            self.root = self.get_root()
        return self.env_class.create(self, request=request, **kwargs)

#    def __call__(self, environ, start_response):
#        if environ['PATH_INFO']=='/':
#            import cProfile
#            pr = cProfile.Profile()
#            pr.enable()
#            #import time
#            #s = time.time()
#            try:
#                return BaseApplication.__call__(self, environ, start_response)
#            finally:
#                pr.disable()
#                pr.dump_stats('stat')
#            #     e = time.time()
#            #    print 'time: %s' % (e-s)
#        return BaseApplication.__call__(self, environ, start_response)

    class i18n_cls(BaseApplication.i18n_cls):
        def set_active_lang(self, env, active):
            BaseApplication.i18n_cls.set_active_lang(self, env, active)
            env.sections = env.sections[active]

