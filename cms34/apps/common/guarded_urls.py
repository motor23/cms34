# coding: utf-8

from iktomi import web
from iktomi.web import URL
from webob.exc import HTTPMovedPermanently, HTTPMethodNotAllowed, HTTPNotFound, HTTPBadRequest


class GuardedRequest(object):
    # TODO: Move implementation from kremlin or remove class usage from project
    def __init__(self):
        raise NotImplemented()


class fix_slash_match(web.match):

    def match(self, env, data):
        path = env._route_state.path
        s_request, s_match = path.endswith('/'), self.url.endswith('/')
        if s_request and not s_match:
            matched, kwargs = self.builder.match(path.rstrip('/'), env=env)
            if matched is not None:
                url = URL.from_url(env.request.url)
                url = url._copy(path=url.path.rstrip('/'))
                return HTTPMovedPermanently(location=url)
        elif not s_request and s_match:
            matched, kwargs = self.builder.match(path + '/', env=env)
            if matched is not None:
                url = URL.from_url(env.request.url)
                url = url._copy(path=url.path + '/')
                return HTTPMovedPermanently(location=url)
        else:
            return web.match.__call__(self, env, data)
    __call__ = match  # for beautiful traceback`s


class guard(web.WebHandler):
    """
        params:    None - do not check anything
                         dict - {key: type}

        methods:  if request.method not in methods, throws MethodNotAllowed
    """

    def __init__(self, methods=('GET',), params=(), xsrf_check=True):
        if params is not None:
            params = dict(params)
        self.params = params

        methods = list(methods)
        if 'GET' in methods and not 'HEAD' in methods:
            methods.append('HEAD')
        self.methods = methods
        self.xsrf_check = xsrf_check

    def guard(self, env, data):
        # XXX a syntax for multiple attributes
        request = env.request
        if isinstance(request, GuardedRequest):
            request = request.unwrap()
        if request.method not in self.methods:
            raise HTTPMethodNotAllowed()

        # we can skip parameters validation for cached views because
        # their usage is restricted by @cache wrapping request into a
        # GuardedRequest
        if self.params or (self.params is not None and
                               not isinstance(env.request, GuardedRequest)):
            checked_args = set()
            for key, value in request.GET.items():
                if key.startswith('utm_') or key.startswith('hc_'):
                    continue
                if key in checked_args or key not in self.params:
                    raise HTTPNotFound()
                checked_args.add(key)
                tp = self.params[key]
                if type(tp) in (list, tuple):
                    if value and not value in tp:
                        raise HTTPNotFound
                elif value and tp is not None and tp != "":
                    try:
                        tp(value)
                    except ValueError: # XXX write validation
                        raise HTTPNotFound()
        if request.method == 'POST' and self.xsrf_check:
            xsrf_token1 = request.POST.get('sid', u'')
            xsrf_token2 = request.cookies.get('sid', u'')
            if not xsrf_token1 or xsrf_token1 != xsrf_token2:
                message = env.gettext(u'Для отправки формы браузер '
                                      u'должен поддерживать JavaScript и Cookie')
                return HTTPBadRequest(message)

        return self.next_handler(env, data)
    __call__ = guard


def GuardedRule(path, handler, methods=('GET',), params=(),
                name=None, convs=None):
    # werkzeug-style Rule
    if name is None:
        name = handler.func_name
    h = fix_slash_match(path, name, convs=convs)
    return h | guard(methods, params) | handler


Rule = GuardedRule


def GuardedMatch(path, name, convs=None, methods=('GET',), params=()):
    return web.match(path, name, convs=convs) | guard(methods, params)
