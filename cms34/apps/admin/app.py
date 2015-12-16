# -*- coding:utf8 -*-
from iktomi.utils import cached_property
from iktomi.unstable.db.files import FileManager

from ..common.app import Application as BaseApplication
from ..common.sessionmakers import binded_filesessionmaker
from ..common.cli import AppCliDict, AppCli, FcgiCli, DbCli
from ..common.dispatcher import DispatcherApp


class AppCli(AppCli):
    name = 'admin'

class FcgiCli(FcgiCli):
    name = 'admin_fcgi'


class Application(BaseApplication):

    properties = [
        'template_engine',
        'cache',
        'models',
#        'admin_models',
#        'front_models',
#        'shared_models',
#        'flood_models',
#        'query_class',
        'admin_file_manager',
        'front_file_manager',
        'shared_file_manager',
        'private_file_manager',
        'db_maker',

        'streams',
        'dashboard',
        'top_menu',

        'front_app_class',
        'preview_app_overload',
        'preview_app',

        'env_class',
        'handler',
        'root',
    ]
    cli_dict = AppCliDict([AppCli, FcgiCli, DbCli])
    preview_app_class = None

    @classmethod
    def cfg_class(cls):
        from .cfg import Cfg
        return Cfg


    class Dispatcher(DispatcherApp):
        @classmethod
        def cfg_class(cls):
            from .cfg import DispatcherCfg
            return DispatcherCfg
 
    def get_streams(env):
        from .streams import streams
        return streams

    def get_dashboard(env):
        from .menuconf import dashboard
        return dashboard

    def get_top_menu(env):
        from .menuconf import top_menu
        return top_menu

    def get_handler(self):
        from .handler import create_handler
        return create_handler(self)

    def get_env_class(self):
        from .environment import Environment
        return Environment

    def get_db_maker(self):
        return binded_filesessionmaker(self.cfg.DATABASES,
                        engine_params=self.cfg.DATABASE_PARAMS,
                        default_file_manager=self.admin_file_manager,
                        file_managers={
                            self.models.admin.metadata: self.admin_file_manager,
                            self.models.front.metadata: self.front_file_manager,
                            self.models.shared.metadata: self.shared_file_manager,
                        })


    def get_admin_file_manager(self):
        return FileManager(
            transient_root=self.cfg.ADMIN_FORM_TMP_DIR,
            persistent_root=self.cfg.ADMIN_MEDIA_DIR,
            transient_url=self.cfg.ADMIN_FORM_TMP_URL,
            persistent_url=self.cfg.ADMIN_MEDIA_URL,
        )

    def get_front_file_manager(self):
        return FileManager(
            transient_root=None,
            persistent_root=self.cfg.FRONT_MEDIA_DIR,
            transient_url=None,
            persistent_url=self.cfg.ADMIN_MEDIA_URL,
        )

    def get_shared_file_manager(self):
        return FileManager(
            transient_root=self.cfg.SHARED_FORM_TMP_DIR,
            persistent_root=self.cfg.SHARED_MEDIA_DIR,
            transient_url=None,
            persistent_url=self.cfg.SHARED_MEDIA_URL,
        )

    def get_private_file_manager(self):
        return FileManager(
            transient_root=self.cfg.PRIVATE_FORM_TMP_DIR,
            transient_url=None,
            persistent_root=self.cfg.PRIVATE_MEDIA_DIR,
            persistent_url=self.cfg.PRIVATE_MEDIA_URL,
        )

    preview_enabled = False

    @classmethod
    def preview_cfg_overload(cls):
        from .preview import PreviewCfgOverload
        return PreviewCfgOverload

    def get_front_app_class(self):
        from ..front import Application
        return Application

    def get_preview_app_overload(self):
        from .preview import PreviewAppOverload
        return PreviewAppOverload

    def get_preview_app(self):
        front_cfg_class = self.front_app_class.cfg_class()
        preview_cfg = type('Cfg',
                           (self.preview_cfg_overload(), front_cfg_class),
                           {})(self.cfg)

        preview_app = type('Application',
                           (self.preview_app_overload, self.front_app_class),
                           {})(preview_cfg, self)
        return preview_app


    def create_environment(self, request=None, **kwargs):
        self.handler = self.get_handler()
        self.root = self.get_root()
        env= BaseApplication.create_environment(self,
                                                request=request, **kwargs)
        return env
