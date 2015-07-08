# -*- coding:utf8 -*-
from iktomi.utils import cached_property
from iktomi.unstable.db.files import FileManager, ReadonlyFileManager
from iktomi.unstable.db.sqla.public_query import PublicQuery

from ..common.app import Application as BaseApplication
from ..common.sessionmakers import binded_filesessionmaker
from ..common.i18n import I18n as I18n
from ..common.cli import AppCliDict, AppCli, FcgiCli, WatchCli
from ..common.dispatcher import DispatcherApp


class AppCli(AppCli):
    name = 'front'

class FcgiCli(FcgiCli):
    name = 'front_fcgi'


class Application(BaseApplication):

    cli_dict = AppCliDict([AppCli, FcgiCli, WatchCli])

    class Dispatcher(DispatcherApp):
        @classmethod
        def cfg_class(cls):
            from .cfg import DispatcherCfg
            return DispatcherCfg

    @classmethod
    def cfg_class(cls):
        from .cfg import Cfg
        return Cfg

    @cached_property
    def handler(self):
        from .handler import create_handler
        return create_handler(self)

    @cached_property
    def env_class(self):
        from .environment import Environment
        return Environment

    @cached_property
    def front_models(self):
        return self.models.front

    @cached_property
    def shared_models(self):
        return self.models.shared

    @cached_property
    def flood_models(self):
        return self.models.flood

    query_class = PublicQuery

    @cached_property
    def db_maker(self):
        return binded_filesessionmaker(self.cfg.DATABASES,
                    engine_params=self.cfg.DATABASE_PARAMS,
                    session_params={'query_cls': self.query_class},
                    default_file_manager=self.front_file_manager,
                    file_managers={
                        self.front_models.metadata: self.front_file_manager,
                        self.shared_models.metadata: self.shared_file_manager,
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

    @cached_property
    def i18n(self):
        return self.i18n_cls(['ru', 'en'],
                    translations_dir=self.cfg.I18N_TRANSLATIONS_DIR,
                    categories=['front', 'iktomi-forms'])


    class i18n_cls(I18n):
        def set_active_lang(self, env, active):
            I18n.set_active_lang(self, env, active)
            env._models = env.models
            env.models = getattr(env.models, active)
            env._shared_models = env.shared_models
            env.shared_models = getattr(env.shared_models, active)

