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
        result = self.app.handle(app_env, data)
        app_env.finalize()
        return result


def h_app(prefix, name, app):
    return web.prefix(prefix, name=name) | H_App(app)
