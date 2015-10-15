# -*- coding: utf8 -*-
import os
import sys
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
    DEFAULT_CUSTOM_CFG = None

    def __init__(self, **kwargs):
        self._init_kwargs = kwargs
        self.update_cfg(kwargs)

    def update_cfg(self, kwargs):
        self.__dict__.update(kwargs)

    def update_from_py(self, filepath=None, silent=True):
        filepath = filepath or self.DEFAULT_CUSTOM_CFG
        if silent and not os.path.isfile(filepath):
            return
        l = {}
        execfile(filepath, dict(cfg=self), l)
        self.update_cfg(l)
        for key, value in l.items():
            setattr(self, key, value)
        return self


class Cfg(BaseCfg):
    APP_ID = 'cms34_app'

    @cached_property
    def ROOT(self):
        # May cause problems when running app with uWSGI,
        # need to pass ROOT explicitly (see `uwsgi_admin.py`).
        return os.path.dirname(os.path.abspath(__main__.__file__))

    @cached_property
    def SITE_DIR(self):
        raise NotImplementedError

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

    @cached_property
    def FRONT_BUILD_DIR(self):
        return os.path.join(self.ROOT, 'build')

    DOMAINS = []

    EMAIL_ERRORS_TO = []
    EMAIL_LETTERS_TO = []

    UID = 'someuid'

    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s: %(levelname)-5s: %(name)-15s: %(message)s'
    SQLALCHEMY_LOG_LEVEL = 'WARNING'
    SQLALCHEMY_ENGINE_LOG_LEVEL = 'WARNING'
    SQLALCHEMY_POOL_LOG_LEVEL = 'WARNING'

    DEV_STATIC = False

    @cached_property
    def STATIC_DIR(self):
        return os.path.join(self.SITE_DIR, 'static')

    @cached_property
    def DEV_STATIC_DIR(self):
        return os.path.join(self.SITE_DIR, 'dev_static')

    SMTP_PORT = 25
    SMTP_HOST = "localhost"
    SMTP_CHARSET = "utf-8"
    SMTP_FROM = "noreply@mail.gov.ru"

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
            fastcgi_params=self.FASTCGI_PARAMS,
            umask=0,
            bind=path.join(self.RUN_DIR, 'app.sock'),
            pidfile=path.join(self.RUN_DIR, 'app.pid'),
            logfile=path.join(self.LOG_DIR, 'app.log'),
        )

    def config_uid(self):
        if os.getuid():
            return
        try:
            os.setgroups([])
            p = pwd.getpwnam(self.UID)
            uid = p[2]
            gid = p[3]
            os.setgid(gid)
            os.setegid(gid)
            os.setuid(uid)
            os.seteuid(uid)
        except AttributeError:
            sys.exit('UID and GID configuration variables are required ' \
                     'when is launched as root')

    def config_logging(self):
        lvl_names = logging._levelNames
        logging.basicConfig(
            level=lvl_names[self.LOG_LEVEL],
            format=self.LOG_FORMAT)

        logging.getLogger('sqlalchemy') \
            .setLevel(lvl_names[self.SQLALCHEMY_LOG_LEVEL])
        logging.getLogger('sqlalchemy.engine') \
            .setLevel(lvl_names[self.SQLALCHEMY_ENGINE_LOG_LEVEL])
        logging.getLogger('sqlalchemy.pool') \
            .setLevel(lvl_names[self.SQLALCHEMY_POOL_LOG_LEVEL])
