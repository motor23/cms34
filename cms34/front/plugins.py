from webob.exc import HTTPNotFound, HTTPSeeOther
from cms34.stream import FilterFormFactory
from .view import Context


class ViewPlugin(object):
    def __init__(self, view):
        self.env = view.env
        self.view = view
        self.c = Context(self.env, '%s_%s' % (self.view.c._key, self.name))


class VP_Query(ViewPlugin):
    model = None
    name = 'query'
    order_field = 'id'
    order_asc = True
    limit = None

    @property
    def query(self):
        return self._query(self.env)

    def get_or_404(self, **kwargs):
        return self._get_or_404(self.env, **kwargs)

    def get_model(self, name=None):
        return self._get_model(self.env, name=name)

    @classmethod
    def _models(cls, env):
        return env.models

    @classmethod
    def _get_model(cls, env, name=None):
        return getattr(cls._models(env), name or cls.model)

    @classmethod
    def _get_order(cls, env):
        field = getattr(cls._get_model(env), cls.order_field)
        if cls.order_asc:
            return field.asc()
        else:
            return field.desc()

    @classmethod
    def _base_query(cls, env):
        return env.db.query(cls._get_model(env))

    @classmethod
    def _query(cls, env):
        query = cls._base_query(env).order_by(cls._get_order(env))
        if cls.limit:
            query = query.limit(cls.limit)
        return query

    @classmethod
    def _get_or_404(cls, env, **kwargs):
        obj = cls._base_query(env).filter_by(**kwargs).first()
        if obj is None:
            raise HTTPNotFound()
        return obj

    def __call__(self):
        return self.query


class VP_Response(ViewPlugin):
    name = 'response'

    @property
    def templates_folder(self):
        return self.view.name

    def template_name(self, template):
        folders = [self.templates_folder]
        # parent = self.view.parent
        # while parent:
        #    folders.insert(0, parent.response.templates_folder)
        #    parent = parent.parent
        return '%s/%s' % ('/'.join(folders), template)

    def template(self, template, kwargs):
        if isinstance(template, basestring):
            kwargs.setdefault('view', self.view)
            return self.view.env.render_to_response(
                self.template_name(template),
                kwargs)
        else:
            return template.render(self.view, kwargs)

    def redirect_to(self, reverse, qs, **kwargs):
        url = reverse.as_url
        if qs:
            url = url.qs_set(qs)
        return HTTPSeeOther(location=str(url))

    def string(self, template, kwargs):
        kwargs.setdefault('view', self.view)
        return self.view.env.render_to_string(self.template_name(template),
                                              kwargs)


class VP_Filter(ViewPlugin):
    name = 'filter'
    Factory = FilterFormFactory
    initials = {}
    active = False

    def init(self, initials={}, **kwargs):
        factory = self.Factory(view=self.view, **kwargs)
        initials = dict(self.initials, **initials)
        self.c.form = factory(self.env, None, initials)
        self.active = True

    def get_form(self):
        try:
            return self.c.form
        except AttributeError:
            self.init()
            return self.c.form

    def accept(self, data=None):
        if data is None:
            data = self.env.request.GET
        return self.get_form().accept(data)

    def filter(self, query):
        return self.get_form().filter(query)

    def __call__(self, query):
        return self.filter(query)

    def render(self):
        return self.get_form().render()

    @property
    def is_valid(self):
        return self.get_form().is_valid
