# -*- coding:utf8 -*-
from iktomi.utils import cached_property
from iktomi.cms.menu import (Menu, DashStream)

from ..common.app import Application as BaseApplication
from ..common.sessionmakers import binded_filesessionmaker
from ..common.files import FileManager


class Application(BaseApplication):

    @cached_property
    def streams(env):
        from .streams import streams
        return streams

    @cached_property
    def dashboard(env):
        from .menuconf import dashboard
        return dashboard

    @cached_property
    def top_menu(env):
        from .menuconf import top_menu
        return top_menu

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import AdminEnvironment
        return AdminEnvironment


    def command_admin(self):
        from iktomi.cli.app import App
        shell_namespace = {
            'app': self,
            'db': self.db_maker(),
        }
        return App(self, shell_namespace=shell_namespace)

    def command_admin_fcgi(self):
        from iktomi.cli.fcgi import Flup
        return Flup(self, **self.cfg.FLUP_ARGS)

    def command_db(self):
        import models.initial
        from models import metadata_dict
        from iktomi.cli.sqla import Sqla
        return Sqla(self.db_maker, metadata_dict,
                    initial=models.initial.install)


    @cached_property
    def db_maker(self):
        import models
        return binded_filesessionmaker(self.cfg.DATABASES,
                                   engine_params=self.cfg.DATABASE_PARAMS,
                                   default_file_manager=self.file_manager,
                                   file_managers={
                                       models.shared.metadata: self.shared_file_manager,
                                   })


    @cached_property
    def file_manager(self):
        return FileManager(
            transient_root=self.cfg.ADMIN_FORM_TMP_DIR,
            persistent_root=self.cfg.ADMIN_MEDIA_DIR,
            transient_url=self.cfg.ADMIN_FORM_TMP_URL,
            persistent_url=self.cfg.ADMIN_MEDIA_URL,
            public_root=self.cfg.FRONT_MEDIA_DIR,
        )

    @cached_property
    def shared_file_manager(self):
        return FileManager(
            transient_root=self.cfg.SHARED_FORM_TMP_DIR,
            persistent_root=self.cfg.SHARED_MEDIA_DIR,
            persistent_url=self.cfg.SHARED_MEDIA_URL,
        )

    @cached_property
    def private_file_manager(self):
        return FileManager(
            transient_root=self.cfg.PRIVTE_FORM_TMP_DIR,
            transient_url=None,
            persistent_root=self.cfg.PRIVTE_MEDIA_DIR,
            persistent_url=self.cfg.PRIVTE_MEDIA_URL,
        )
