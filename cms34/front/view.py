from collections import OrderedDict
from iktomi.web import WebHandler, cases as cases


class HView(WebHandler):

    def __init__(self, view_cls, **kwargs):
        assert view_cls.name is not None, 'You must set context name'
        self.view_cls = view_cls
        self.kwargs = kwargs

    def view(self, env, data):
        view = self.view_cls(env, data, **self.kwargs)
        views = getattr(env, 'views', [])
        views.append(view)
        env.views = views
        env.view = view
        return self.next_handler(env, data)
    __call__ = view


class Context(object):

    def __init__(self, env, key):
        self._env = env
        self._key = key

    def __getattr__(self, name):
        if name[0]=='_':
            return object.__getattribute__(self, name)
        return getattr(self._env, self._get_prop_key(name))

    def __setattr__(self, name, value):
        if name[0]=='_':
            return object.__setattr__(self, name, value)
        setattr(self._env, self._get_prop_key(name), value)

    def _get_prop_key(self, prop_name):
        return '%s_%s' % (self._key, prop_name)


class BaseView(object):

    name = None
    plugins = []

    def __init__(self, env, data):
        self.env = env
        self.data = data
        self.namespace = env.namespace
        subreverse = env.root.build_subreverse(self.namespace,
                                               **data.as_dict())
        if not subreverse._ready:
            subreverse = subreverse(**data.as_dict())
        self.root = subreverse
        self.parent = getattr(env, 'view', None)
        self.c = Context(env, 'view_context_%s' % self.namespace)
        plugins = []
        for plugin in self.plugins:
            assert not hasattr(self, plugin.name), \
                   'property %s already exists' % plugin.name
            p = plugin(self)
            plugins.append(p)
            setattr(self, plugin.name, p)
        self.plugins = plugins

    def result(self, env, data, result):
        for plugin in self.plugins:
            result = plugin(result)
        return result

    @classmethod
    def cases(cls):
        return []

    @classmethod
    def handler(cls):
        return HView(cls) | cases(*cls.cases())

    def url_for_index(self):
        return self._url_for_index(self.root)

    def url_for_obj(self, obj):
        return self._url_for_obj(self.root, obj)

    @classmethod
    def _url_for_index(cls, root):
        return None

    @classmethod
    def _url_for_obj(cls, root, obj):
        return None


class ViewHandler(WebHandler):

    def __init__(self, method):
        self.method = method

    def __call__(self, env, data):
        result = self.method(env.view, env, data)
        return result or self.next_handler(env, data)


def view_handler(method):
    return ViewHandler(method)


