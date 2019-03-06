import sys
from subprocess import Popen
import os.path
import fnmatch
from multiprocessing import Process
from iktomi.cli.app import wait_for_code_change
from iktomi.cli.app import flush_fds
from iktomi.cli.app import MAXFD
from iktomi.cli.base import Cli as BaseCli
from iktomi.cli.app import App as BaseApp
from iktomi.cli.fcgi import Flup as BaseFcgi
from iktomi.cli.sqla import Sqla as BaseDb

from .dispatcher import DispatcherApp


class AppCliDict(object):
    def __init__(self, cli_classes):
        self.cli_classes = cli_classes

    def __get__(self, app, app_cls):
        return dict([(cli_cls.name, cli_cls(app_cls))
                     for cli_cls in self.cli_classes])


class Cli(BaseCli):
    name = None

    def __init__(self, App):
        self.App = App

    def create_cfg(self, custom_cfg_path=None, **kwargs):
        cfg = self.App.cfg_class()(**kwargs)
        return cfg.update_from_py(custom_cfg_path)

    def create_app(self, cls, level=None, **kwargs):
        app = cls.custom(**kwargs)
        if level:
            app.cfg.LOG_LEVEL = level
        app.cfg.config_uid()
        app.cfg.config_logging()
        return app


class AppCli(Cli):
    name = 'app'
    DEFAULT_PORT = '8000'

    def  command_serve(self, host='', port=None, level=None, cfg=''):
        def http_process(host, port, stdin):
            sys.stdin = stdin
            from wsgiref.simple_server import make_server
            app = self.create_app(self.App, level=level, custom_cfg_path=cfg)
            host = host or app.cfg.HTTP_SERVER_HOST
            if port is None:
                port = getattr(app.cfg, 'HTTP_SERVER_PORT', self.DEFAULT_PORT)
            print('Staring HTTP server {}:{}...'.format(host, port))
            server = make_server(host, port, app)
            server.serve_forever()

        stdin = os.fdopen(os.dup(sys.stdin.fileno()))
        p1 = Process(target=http_process, args=(host, port, stdin))
        p1.start()

        cfg = self.create_cfg()

        extra_files = []
        for root, dirnames, filenames in os.walk(cfg.ROOT):
            for filename in fnmatch.filter(filenames, '*.py'):
                extra_files.append(os.path.join(root, filename))

        try:
            wait_for_code_change(extra_files=extra_files)
            p1.terminate()
            p1.join()
            flush_fds()

            pid = os.fork()
            if pid:
                os.closerange(3, MAXFD)
                os.waitpid(pid, 0)
                os.execvp(sys.executable, [sys.executable] + sys.argv)
            else:
                sys.exit()

        except KeyboardInterrupt:
            print('Terminating HTTP server...')
            p1.terminate()

        sys.exit()


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
        return BaseApp(
            app,
            shell_namespace=self.shell_namespace(app),
            extra_files=(app.cfg.DEFAULT_CUSTOM_CFG,)
        )


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

    def command_stop_dispatcher(self, level=None, cfg=''):
        app = self.create_app(self.App.Dispatcher,
                              App=self.App, level=level, custom_cfg_path=cfg)
        return self.cli(app, **app.cfg.FLUP_ARGS).command_stop()

    def cli(self, app, **kwargs):
        return BaseFcgi(app, **kwargs)


class DbCli(Cli):
    name = 'db'

    def create_app(self, cls, level=None, **kwargs):
        """
        We do not want to initialize full application here, only base app
        properties needed. Full app initializes sections from DB, so we will
        fail because of inconsistent model-schema state.
        """
        cls.properties = [
            'models',
            'admin_file_manager',
            'front_file_manager',
            'shared_file_manager',
            'db_maker',
            'env_class',
        ]
        return super(DbCli, self).create_app(cls, level, **kwargs)

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

    def cli(self, app):
        import models.initial
        from models import metadata_dict
        return BaseDb(app.db_maker, metadata_dict,
                      initial=models.initial.install)


class WatchCli(Cli):
    name = 'watch'

    css_watch_command = 'watch-css'
    js_watch_command = 'watch-js'
    all_watch_command = 'watch-all'

    def gulp(self, task, cfg, wait=False):
        gulp_executable = '{}/node_modules/.bin/gulp'.format(
            cfg.FRONT_BUILD_DIR)
        if not os.path.isfile(gulp_executable):
            print "Gulp executable not found. Install Gulp with `npm install`."
            sys.exit(0)

        command = '{gulp} --gulpfile={gulpfile} {task}'.format(
            gulp=gulp_executable, gulpfile=cfg.GULP_FILE, task=task)

        try:
            p = Popen(command, shell=True)
            if wait:
                print "To stop watching, use CTRL-C"
                p.wait()
        except Exception:
            p.kill()
            raise
        except (KeyboardInterrupt, SystemExit):
            print "Stop watching"

    def command_css(self, cfg=''):
        app_cfg = self.create_cfg(custom_cfg_path=cfg)
        self.gulp(self.css_watch_command, app_cfg, wait=True)

    def command_js(self, cfg=''):
        app_cfg = self.create_cfg(custom_cfg_path=cfg)
        self.gulp(self.js_watch_command, app_cfg, wait=True)

    def command_all(self, cfg=''):
        app_cfg = self.create_cfg(custom_cfg_path=cfg)
        self.gulp(self.all_watch_command, app_cfg, wait=True)
