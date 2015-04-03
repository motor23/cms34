# -*- coding:utf8 -*-
from iktomi.utils import cached_property
from iktomi.unstable.db.files import FileManager, ReadonlyFileManager
from iktomi.unstable.db.sqla.public_query import PublicQuery

from ..common.app import Application as BaseApplication
from ..common.sessionmakers import binded_filesessionmaker


class Application(BaseApplication):

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import Environment
        return Environment

    def command_front(self):
        from iktomi.cli.app import App
        shell_namespace = {
            'app': self,
            'db': self.db_maker(),
        }
        return App(self, shell_namespace=shell_namespace)

    def command_front_fcgi(self):
        from iktomi.cli.fcgi import Flup
        return Flup(self, **self.cfg.FLUP_ARGS)

    @cached_property
    def db_maker(self):
        import models
        return binded_filesessionmaker(self.cfg.DATABASES,
                        engine_params=self.cfg.DATABASE_PARAMS,
                        session_params={'query_cls': PublicQuery},
                        default_file_manager=self.front_file_manager,
                        file_managers={
                            models.front.metadata: self.front_file_manager,
                            models.shared.metadata: self.shared_file_manager,
                        })

    @cached_property
    def front_file_manager(self):
        return ReadonlyFileManager(
            persistent_root=self.cfg.FRONT_MEDIA_DIR,
            persistent_url=self.cfg.FRONT_MEDIA_URL,
        )

    @cached_property
    def shared_file_manager(self):
        return FileManager(
            transient_root=self.cfg.SHARED_FORM_TMP_DIR,
            persistent_root=self.cfg.SHARED_MEDIA_DIR,
            transient_url=None,
            persistent_url=None,
        )

