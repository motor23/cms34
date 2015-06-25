from iktomi import web

class H_App(web.WebHandler):

    def __init__(self, app):
        self.app = app
        self._next_handler = self.app.handler

    def __call__(self, env, data):
        subreverse = env.root.build_subreverse(env.namespace,
                                               **data.as_dict())
        app_env = self.app.create_environment(
            root=subreverse,
            request=env.request,
            route_state=env._route_state,
            parent_env=env,
        )
        app_env._route_state = env._route_state
        return self.app.handle(app_env, data)


def h_app(prefix, name, app):
    return web.prefix(prefix, name=name) | H_App(app)
