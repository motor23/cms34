# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import static_files, prefix, cases, namespace
from ..common.caching import Caching, cache

from .views import h_index

__all__ = ['create_handler']


def create_handler(app):
    h_caching = Caching(app.cache, duration=app.cfg.CACHE_TIME)

    return cases(
        static_files(app.cfg.STATIC_DIR, app.cfg.STATIC_URL),
        static_files(app.cfg.FRONT_MEDIA_DIR, app.cfg.MEDIA_URL),

        h_caching | cache(enable=app.cfg.CACHE_ENABLED) | cases(
            prefix('/en') | app.i18n.handler('en') | h_index,
            app.i18n.handler('ru') | h_index,
        ),
        HTTPNotFound,
)
