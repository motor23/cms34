# -*- coding: utf-8 -*-
from os import path
from collections import OrderedDict
import iktomi.templates, iktomi.cms
from cms34.utils import cached_property
from ..common.cfg import Cfg as CfgBase
from ..common.dispatcher import Cfg as DispatcherCfgBase


class Cfg(CfgBase):
    @cached_property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'admin.py')

    @cached_property
    def SITE_DIR(self):
        return path.join(self.ROOT, 'admin')

    IKTOMI_TEMPLATE_DIR = path.dirname(path.abspath(iktomi.templates.__file__))
    IKTOMI_CMS_DIR = path.dirname(path.abspath(iktomi.cms.__file__))
    CMS34_DIR = path.dirname(path.abspath(__file__))

    @cached_property
    def TEMPLATES(self):
        return [
            path.join(self.SITE_DIR, 'templates'),
            path.join(self.CMS34_DIR, 'templates'),
            path.join(self.IKTOMI_CMS_DIR, 'templates'),
            path.join(self.IKTOMI_TEMPLATE_DIR, 'jinja2', 'templates'),
        ]

    @cached_property
    def CMS_STATIC_DIR(self):
        return path.join(self.IKTOMI_CMS_DIR, 'static')

    CMS_STATIC_URL = '/cms-static/'

    @cached_property
    def CMS34_STATIC_DIR(self):
        return path.join(self.CMS34_DIR, 'static')

    CMS34_STATIC_URL = '/cms34-static/'
    STATIC_URL = '/static/'

    @cached_property
    def ADMIN_FORM_TMP_DIR(self):
        return path.join(self.TMP_DIR, 'admin')

    PRIVATE_FORM_TMP_DIR = ADMIN_FORM_TMP_DIR
    SHARED_FORM_TMP_DIR = ADMIN_FORM_TMP_DIR

    @cached_property
    def PRIVATE_MEDIA_DIR(self):
        return path.join(self.MEDIA_DIR, 'private')

    ADMIN_MEDIA_URL = '/media/'
    SHARED_MEDIA_URL = '/shared/'
    PRIVATE_MEDIA_URL = '/private/'
    ADMIN_FORM_TMP_URL = '/form-temp/'

    MODEL_LOCK_TIMEOUT = 5 * 60
    MODEL_LOCK_RENEW = 60

    @cached_property
    def FLUP_ARGS(self):
        return dict(
            fastcgi_params=self.FASTCGI_PARAMS,
            umask=0,
            bind=path.join(self.RUN_DIR, 'admin.sock'),
            pidfile=path.join(self.RUN_DIR, 'admin.pid'),
            logfile=path.join(self.LOG_DIR, 'admin.log'),
        )

    @cached_property
    def STATIC_DIR(self):
        return path.join(self.SITE_DIR, 'static')

    @cached_property
    def MANIFESTS(self):
        return OrderedDict([
            ("cms", {
                "path": self.CMS_STATIC_DIR,
                "url": self.CMS_STATIC_URL,
                "css": 'css/Manifest',
                "js": 'js/Manifest'
            }),
            ("cms34", {
                "path": self.CMS34_STATIC_DIR,
                "url": self.CMS34_STATIC_URL,
                "css": 'css/Manifest',
                "js": 'js/Manifest'
            }),
            ('local', {
                "path": self.STATIC_DIR,
                "url": self.STATIC_URL,
                "css": 'css/Manifest',
                "js": 'js/Manifest'
            })
        ])

    MEMCACHE = ['127.0.0.1:11211']
    CACHE_PREFIX = 'admin'

    DATABASES = {
        'admin': 'mysql://root@localhost/admin?charset=utf8',
        'front': 'mysql://root@localhost/front?charset=utf8',
        'shared': 'mysql://root@localhost/shared?charset=utf8',
        'flood': 'mysql://root@localhost/flood?charset=utf8',
    }

    DATABASE_PARAMS = {
        'pool_size': 10,
        'max_overflow': 50,
        'pool_recycle': 3600,
    }


class DispatcherCfg(DispatcherCfgBase):
    @cached_property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'dispatcher_admin.py')

    @cached_property
    def FLUP_ARGS(self):
        return dict(
            fastcgi_params=self.FASTCGI_PARAMS,
            umask=0,
            bind=path.join(self.RUN_DIR, 'admin.sock'),
            pidfile=path.join(self.RUN_DIR, 'admin.pid'),
            logfile=path.join(self.LOG_DIR, 'admin.log'),
        )
