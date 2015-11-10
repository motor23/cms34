# -*- coding: utf-8 -*-
from os import path
import sys
import memcache
from collections import OrderedDict
from cms34.utils import cached_property
from ..common.cfg import Cfg as CfgBase
from ..common.dispatcher import Cfg as DispatcherCfgBase


class Cfg(CfgBase):
    @cached_property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'front.py')

    @cached_property
    def SITE_DIR(self):
        return path.join(self.ROOT, 'front')

    CMS34_DIR = path.dirname(path.abspath(__file__))

    @cached_property
    def TEMPLATES(self):
        return [
            path.join(self.SITE_DIR, 'templates'),
            path.join(self.CMS34_DIR, 'templates'),
        ]

    MEDIA_URL = FRONT_MEDIA_URL = '/media/'

    @cached_property
    def SHARED_FORM_TMP_DIR(self):
        return path.join(self.TMP_DIR, 'shared')

    MODEL_LOCK_TIMEOUT = 5 * 60
    MODEL_LOCK_RENEW = 60

    @cached_property
    def FLUP_ARGS(self):
        return dict(
            fastcgi_params=self.FASTCGI_PARAMS,
            umask=0,
            bind=path.join(self.RUN_DIR, 'front.sock'),
            pidfile=path.join(self.RUN_DIR, 'front.pid'),
            logfile=path.join(self.LOG_DIR, 'front.log'),
        )

    @cached_property
    def MANIFESTS(self):
        return OrderedDict([
            ("", {
                "css": path.join(SITE_DIR, 'static/css/Manifest'),
                "js": path.join(SITE_DIR, 'static/js/Manifest'),
            }),
        ])

    MEMCACHE = ['127.0.0.1:11211']
    CACHE_PREFIX = 'front'
    CACHE_ENABLED = True
    CACHE_TIME = 60
    CACHE_BLOCKS_TIME = 60
    CACHE_BLOCKS_ONLY = False

    DATABASES = {
        'front': 'mysql://root@localhost/front?charset=utf8',
        'shared': 'mysql://root@localhost/shared?charset=utf8',
        'flood': 'mysql://root@localhost/flood?charset=utf8',
    }

    DATABASE_PARAMS = {
        'pool_size': 10,
        'max_overflow': 50,
        'pool_recycle': 3600,
    }

    FLOOD_PROTECTION = {
        # activity: (freeTries, initValue, multiplier, timeout)
        'default': (0, 60, 2, 12 * 60 * 60),
        'letters': (3, 60, 2, 12 * 60 * 60),
        'subscribe': (10, 60, 1, 10 * 60),
    }

    FLOOD_PROTECTION_ENABLED = True

    @cached_property
    def GULP_FILE(self):
        return path.join(self.FRONT_BUILD_DIR, 'gulpfile.js')


class DispatcherCfg(DispatcherCfgBase):
    @cached_property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'dispatcher_front.py')

    @cached_property
    def FLUP_ARGS(self):
        return dict(
            fastcgi_params=self.FASTCGI_PARAMS,
            umask=0,
            bind=path.join(self.RUN_DIR, 'front.sock'),
            pidfile=path.join(self.RUN_DIR, 'front.pid'),
            logfile=path.join(self.LOG_DIR, 'front.log'),
        )
