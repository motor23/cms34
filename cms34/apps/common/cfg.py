# -*- coding: utf8 -*-
import os
import sys
import logging
import logging.config

from cms34.utils import cached_property

import __main__

FASTCGI_PREFORKED_DEFAULTS = dict(
    preforked=True,
    multiplexed=False,
    minSpare=1,
    maxSpare=5,
    maxChildren=50,
    maxRequests=0,
)

# Do not change defaults, overwrite params in FASTCGI_PARAMS instead
FASTCGI_THREADED_DEFAULTS = dict(
    preforked=False,
    multithreaded=True,
    multiprocess=False,
    multiplexed=False,
    minSpare=1,
    maxSpare=5,
    maxThreads=sys.maxint,
)


class BaseCfg(object):

    def __init__(self, **kwargs):
        self.update_cfg(kwargs)

    def update_cfg(self, kwargs):
        self.__dict__.update(kwargs)

    def update_from_py(self, filepath, silent=True):
        if silent and not os.path.isfile(filepath):
            return
        l = {}
        execfile(filepath, dict(cfg=self), l)
        self.update_cfg(l)
        for key, value in l.items():
            setattr(self, key, value)

    @classmethod
    def custom(cls, cfg_path=None):
        cfg = cls()
        silent = not bool(cfg_path)
        cfg_path = cfg_path or cfg.DEFAULT_CUSTOM_CFG
        cfg.update_from_py(cfg_path, silent=silent)
        return cfg


class Cfg(BaseCfg):

    def __init__(self, **kwargs):
        BaseCfg.__init__(self, **kwargs)
        self.config_path()
        self.config_uid()

    @cached_property
    def ROOT(self):
        return os.path.dirname(os.path.abspath(__main__.__file__))

    @cached_property
    def SITE_DIR(self):
        raise NotImplementedError

    @cached_property
    def THIRD_PARTY_DIR(self):
        return os.path.join(self.ROOT, 'third-party')

    @cached_property
    def CFG_DIR(self):
        return os.path.join(self.ROOT, 'cfg')

    @cached_property
    def LOG_DIR(self):
        return os.path.join(self.ROOT, 'logs')

    @cached_property
    def RUN_DIR(self):
        return os.path.join(self.ROOT, 'run')

    @cached_property
    def TMP_DIR(self):
        return os.path.join(self.ROOT, 'tmp')

    @cached_property
    def MEDIA_DIR(self):
        return os.path.join(self.ROOT, 'media')

    @cached_property
    def ADMIN_MEDIA_DIR(self):
        return os.path.join(self.MEDIA_DIR, 'admin')

    @cached_property
    def FRONT_MEDIA_DIR(self):
        return os.path.join(self.MEDIA_DIR, 'front')

    @cached_property
    def SHARED_MEDIA_DIR(self):
        return os.path.join(self.MEDIA_DIR, 'shared')

    UID = 'someuid'

    DEV_STATIC = False

    @cached_property
    def STATIC_DIR(self):
        return os.path.join(self.SITE_DIR, 'static')

    @cached_property
    def DEV_STATIC_DIR(self):
        return os.path.join(self.SITE_DIR, 'dev_static')

    STATIC_URL = '/static/'
    DEV_STATIC_URL = '/dev_static/'

    FASTCGI_PARAMS = dict(
        FASTCGI_PREFORKED_DEFAULTS,
        maxSpare=8,
        minSpare=8,
        maxChildren=2,
    )

    @cached_property
    def FLUP_ARGS(self):
        return dict(
            fastcgi_params = self.FASTCGI_PARAMS,
            umask = 0,
            bind = path.join(self.RUN_DIR, 'app.sock'),
            pidfile = path.join(self.RUN_DIR, 'app.pid'),
            logfile = path.join(self.LOG_DIR, 'app.log'),
        )

    def config_path(self):
        for path in [self.THIRD_PARTY_DIR]:
            if path not in sys.path:
                sys.path.insert(0, path)


    def config_uid(uid):
        if os.getuid():
            return
        try:
            os.setgroups([])
            p = pwd.getpwnam(uid)
            uid = p[2]
            gid = p[3]
            os.setgid(gid)
            os.setegid(gid)
            os.setuid(uid)
            os.seteuid(uid)
        except AttributeError:
            sys.exit('UID and GID configuration variables are required '\
                     'when is launched as root')



logging.config.dictConfig({
    'version': 1.0,
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'iktomi.templates': {
            'handlers': ['default'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
})


