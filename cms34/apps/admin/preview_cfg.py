from os import path
from ..common.cfg import BaseCfg

def from_admin_cfg(name):
    return property(lambda self: getattr(self.admin_cfg, name))

class PreviewCfg(BaseCfg):

    def __init__(self, admin_cfg, **kwargs):
        self.admin_cfg = admin_cfg
        BaseCfg.__init__(self, **kwargs)

    PREVIEW = True
    PREFIX = '/preview'

    @property
    def SITE_DIR(self):
        return path.join(self.ROOT, 'front')

    TMP_DIR = from_admin_cfg('TMP_DIR')
    MEDIA_DIR = from_admin_cfg('MEDIA_DIR')
    ADMIN_MEDIA_DIR = from_admin_cfg('ADMIN_MEDIA_DIR')
    FRONT_MEDIA_DIR = from_admin_cfg('FRONT_MEDIA_DIR')
    SHARED_MEDIA_DIR = from_admin_cfg('SHARED_MEDIA_DIR')
    SHARED_FORM_TMP_DIR = from_admin_cfg('SHARED_FORM_TMP_DIR')
    DEV_STATIC = from_admin_cfg('DEV_STATIC')
 
    @property
    def STATIC_URL(self):
        return self.PREFIX + '/static/'

    @property
    def DEV_STATIC_URL(self):
        return self.PREFIX + '/dev_static/'

    CMS34_DIR = path.dirname(path.abspath(__file__))

    CACHE_ENABLED = False
    MEMCACHE = from_admin_cfg('MEMCACHE')
    CACHE_PREFIX = from_admin_cfg('CACHE_PREFIX')

    @property
    def DATABASES(self):
        DATABASES = self.admin_cfg.DATABASES
        DATABASES['front'] = DATABASES['admin']
        return DATABASES

    DATABASE_PARAMS = from_admin_cfg('DATABASE_PARAMS')

    FLOOD_PROTECTION_ENABLED = False

