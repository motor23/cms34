import re
from os import path
import logging

from webob.exc import HTTPNotFound

from ..common.cfg import (
    Cfg as CfgBase,
    FASTCGI_PREFORKED_DEFAULTS,
)

logger = logging.getLogger()


class Cfg(CfgBase):
    DOMAINS = []

    app_cfg_kwargs = {}

    @property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'dispatcher.py')

    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s: %(levelname)-5s: %(name)-15s: %(message)s'
    SQLALCHEMY_LOG_LEVEL = 'WARNING'
    SQLALCHEMY_ENGINE_LOG_LEVEL = 'WARNING'
    SQLALCHEMY_POOL_LOG_LEVEL = 'WARNING'

    def config_logging(self):
        lvl_names = logging._levelNames
        level = lvl_names[self.LOG_LEVEL]
        logging.basicConfig(
            level=level,
            format=self.LOG_FORMAT)
        logging.getLogger().setLevel(level)
        logging.getLogger('sqlalchemy') \
            .setLevel(lvl_names[self.SQLALCHEMY_LOG_LEVEL])
        logging.getLogger('sqlalchemy.engine') \
            .setLevel(lvl_names[self.SQLALCHEMY_ENGINE_LOG_LEVEL])
        logging.getLogger('sqlalchemy.pool') \
            .setLevel(lvl_names[self.SQLALCHEMY_POOL_LOG_LEVEL])


class DispatcherApp(object):
    apps = []

    def __init__(self, App, cfg=None):
        self.cfg = cfg or self.cfg_class()
        self.cfg.config_logging()
        for reg, cfg_path in self.cfg.DOMAINS:
            compiled_reg = re.compile(reg)
            try:
                app = App.custom(cfg_path, ROOT=cfg.ROOT, APP_ID=reg)
                self.apps.append((compiled_reg, app))
            except Exception as e:
                logger.info('Initialization error cfg=%s' % cfg_path)
                logger.exception(e)

    @classmethod
    def custom(cls, App, custom_cfg_path='', **kwargs):
        cfg = cls.cfg_class()(**kwargs)
        # Apply default local config (if any) to app, then apply custom config.
        app_cfg = getattr(App, 'cfg', None)
        if app_cfg:
            cfg.update_from_py(app_cfg.DEFAULT_CUSTOM_CFG)
        cfg.update_from_py(custom_cfg_path)
        return cls(App, cfg)

    @classmethod
    def cfg_class(cls):
        return Cfg

    def __call__(self, environ, start_response):
        try:
            for reg, app in self.apps:
                if reg.match(environ['HTTP_HOST']):
                    return app.__call__(environ, start_response)
            else:
                return HTTPNotFound()(environ, start_response)
        except Exception as e:
            logger.exception(e)
            raise

    def db_maker(self):  # XXX Hack for app:shell
        return None
