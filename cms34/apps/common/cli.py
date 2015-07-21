from subprocess import Popen
import re

from iktomi.cli.base import Cli as BaseCli
from iktomi.cli.app import App as BaseApp
from iktomi.cli.fcgi import Flup as BaseFcgi
from iktomi.cli.sqla import Sqla as BaseDb

from .dispatcher import DispatcherApp


class AppCliDict(object):

    def __init__(self, cli_classes):
        self.cli_classes = cli_classes

    def __get__(self, app, app_cls):
        return dict([(cli_cls.name, cli_cls(app_cls)) \
                                    for cli_cls in self.cli_classes])


class Cli(BaseCli):

    name = None

    def __init__(self, App):
        self.App = App

    def create_cfg(self, custom_cfg_path=None, **kwargs):
        cfg = self.App.cfg_class()(**kwargs)
        return cfg.update_from_py(custom_cfg_path)

    def create_app(self, cls, level=None,  **kwargs):
        app = cls.custom(**kwargs)
        if level:
            app.cfg.LOG_LEVEL = level
        app.cfg.config_uid()
        app.cfg.config_logging()
        return app


class AppCli(Cli):

    name = 'app'

    def command_serve(self, host='', port='8000', level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_serve(host, port)

    def command_dispatch(self, host='', port='8000', level=None, cfg=''):
        app = self.create_app(self.App.Dispatcher,
                              App=self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_serve(host, port)

    def command_shell(self, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_shell()

    def shell_namespace(self, app):
        return {
            'app': app,
            'db': app.db_maker(),
        }

    def cli(self, app):
        return BaseApp(app, shell_namespace=self.shell_namespace(app))


class FcgiCli(Cli):

    name = 'fcgi'

    def command_start(self, daemonize=False, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app, **app.cfg.FLUP_ARGS).command_start(daemonize)

    def command_start_dispatcher(self, daemonize=False, level=None, cfg=''):
        app = self.create_app(self.App.Dispatcher,
                              App=self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app, **app.cfg.FLUP_ARGS).command_start(daemonize)

    def command_stop(self, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app, **app.cfg.FLUP_ARGS).command_stop()

    def cli(self, app, **kwargs):
        return BaseFcgi(app, **kwargs)


class DbCli(Cli):

    name = 'db'

    def command_create_tables(self, meta_name=None, verbose=False,
                              level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_create_tables(meta_name, verbose)

    def command_drop_tables(self, meta_name=None, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_drop_tables(meta_name)

    def command_init(self, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_init()

    def command_reset(self, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_reset()

    def command_schema(self, name=None, level=None, cfg=''):
        app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app).command_schema(name)

    def command_gen(self, *names): #XXX
        app = self.create_app()
        return self.cli(app).command_gen()

    def cli(self, app):
        import models.initial
        from models import metadata_dict
        return BaseDb(app.db_maker, metadata_dict,
                      initial=models.initial.install)


class WatchCli(Cli):

    name = 'watch'

    css_watch_command = 'watch_css'
    js_watch_command = 'watch_js'
    all_watch_command = 'watch_all'

    def grunt(self, task, cfg, wait=False):
        try:
            p = Popen('grunt %s --gruntfile %s' % (task, cfg.GRUNT_FILE),
                      shell=True)
            if wait:
                p.wait()
        except (KeyboardInterrupt, SystemExit):
            p.kill()
            raise

    def command_css(self, cfg=''):
        app_cfg = self.App.cfg_class()()
        app_cfg.update_from_py(cfg)
        self.grunt(self.css_watch_command, app_cfg, wait=True)

    def command_js(self, cfg=''):
        app_cfg = self.App.cfg_class()()
        app_cfg.update_from_py(cfg)
        self.grunt(self.js_watch_command, app_cfg, wait=True)

    def command_all(self, cfg=''):
        app_cfg = self.App.cfg_class()()
        app_cfg.update_from_py(cfg)
        self.grunt(self.all_watch_command, app_cfg, wait=True)

