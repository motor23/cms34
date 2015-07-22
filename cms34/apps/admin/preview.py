from os import path

from iktomi.cms.publishing.model import AdminPublicQuery
from iktomi.utils import cached_property


def from_admin_cfg(name):
    return property(lambda self: getattr(self._admin, name))


class PreviewAppOverload(object):

    def __init__(self, cfg, admin_app, **kwargs):
        self._admin = admin_app
        super(PreviewAppOverload, self).__init__(cfg, **kwargs)

    @property
    def root(self):
        return self._admin.root.build_subreverse('preview')

    def create_environment(self, request=None, **kwargs):
        return self.env_class.create(self, request=request, **kwargs)

    @cached_property
    def front_models(self):
        return self._admin.models.admin

    query_class = AdminPublicQuery


class PreviewCfgOverload(object):

    def __init__(self, admin_cfg):
        self._admin = admin_cfg

    PREVIEW = True
    PREFIX = '/preview'
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

    DATABASES = from_admin_cfg('DATABASES')
    DATABASE_PARAMS = from_admin_cfg('DATABASE_PARAMS')

    FLOOD_PROTECTION_ENABLED = False


