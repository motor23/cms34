from collections import OrderedDict
from iktomi.web import WebHandler, cases as cases


class HView(WebHandler):

    def __init__(self, view_cls, **kwargs):
        assert view_cls.name is not None, 'You must set context name'
        self.view_cls = view_cls
        self.kwargs = kwargs

    def view(self, env, data):
        contexts = dict(getattr(env, 'views_contexts', {}))
        contexts[self.view_cls.name] = {}
        env.view_contexts = contexts

        view = self.view_cls(env, data, **self.kwargs)
        views = getattr(env, 'views', [])
        views.append(view)
        env.views = views
        env.view = view
        return self.next_handler(env, data)
    __call__ = view


class Context(object):

    def __init__(self, env, name):
        self._env = env
        self._name = name

    def __getattr__(self, name):
        if name[0]=='_':
            return object.__getattribute__(self, name)
        context = self.get_context()
        if context.has_attr(name):
            return context[name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name[0]=='_':
            return object.__setattr__(self, name, value)
        context = dict(self.get_context())
        context[name] = value
        self._env.view_contexts[self._name] = context

    def get_context(self):
        return self._env.view_contexts[self._name]


class BaseView(object):

    name = None
    plugins = []

    def __init__(self, env, data):
        self.env = env
        self.namespace = env.namespace
        subreverse = env.root.build_subreverse(self.namespace,
                                               **data.as_dict())
        if not subreverse._ready:
            subreverse = subreverse(**data.as_dict())
        self.root = subreverse
        self.parent = getattr(env, 'view', None)
        self.context = Context(env, self.name)
        for plugin in self.plugins:
            plugin(self)

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
        raise NotImplementedError()

    @classmethod
    def _url_for_obj(cls, root, obj):
        raise NotImplementedError()


class ViewHandler(WebHandler):

    def __init__(self, method):
        self.method = method

    def __call__(self, env, data):
        result = self.method(env.view, env, data)
        return result or self.next_handler(env, data)


def view_handler(method):
    return ViewHandler(method)


