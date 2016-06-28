from iktomi import web


class H_App(web.WebHandler):
    def __init__(self, app):
        self.app = app

    def _locations(self):
        #XXX
        self.app.update_sections(self.app.sections.values(),
                                 dispose_connections=True)
        self.app.handler = self.app.get_handler()
        return self.app.handler._locations()

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


@web.request_filter
def no_preview(env, data, next_handler):
    """
    Forbid access to next handler in preview mode. It can be used for search
    section, for example.
    """
    preview = getattr(env.app.cfg, 'PREVIEW', None)
    if preview:
        return env.render_to_response('nopreview', {})
    return next_handler(env, data)
