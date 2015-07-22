from iktomi import web

class H_App(web.WebHandler):

    def __init__(self, app):
        self.app = app
        self._next_handler = self.app.handler

    def __call__(self, env, data):
        app_env = self.app.create_environment(
            request=env.request,
            route_state=env._route_state,
            parent_env=env,
        )
        try:
            return self.app.handle(app_env, data)
        finally:
            app_env.finalize()


def h_app(prefix, name, app):
    return web.prefix(prefix, name=name) | H_App(app)
