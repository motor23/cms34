import re
from webob.exc import HTTPNotFound

from ..common.cfg import (
    Cfg as CfgBase,
    FASTCGI_PREFORKED_DEFAULTS,
)


class Cfg(CfgBase):
    DOMAINS = []

    app_cfg_kwargs = {}

    @property
    def DEFAULT_CUSTOM_CFG(self):
        return path.join(self.CFG_DIR, 'dispatcher.py')



class DispatcherApp(object):

    apps = []

    def __init__(self, App, cfg=None):
        self.cfg = cfg or self.cfg_class()
        for reg, cfg_path in self.cfg.DOMAINS:
            compiled_reg = re.compile(reg)
            app = App.custom(cfg_path, ROOT=cfg.ROOT)
            self.apps.append((compiled_reg, app))

    @classmethod
    def custom(cls, App, custom_cfg_path='', **kwargs):
        cfg = cls.cfg_class()(**kwargs)
        cfg.update_from_py(custom_cfg_path)
        return cls(App, cfg)

    @classmethod
    def cfg_class(cls):
        return Cfg

    def __call__(self, environ, start_response):
        for reg, app in self.apps:
            if reg.match(environ['HTTP_HOST']):
                return app.__call__(environ, start_response)
        else:
            return HTTPNotFound()(environ, start_response)

    def db_maker(self): #XXX Hack for app:shell
        return None
