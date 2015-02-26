from webob.exc import HTTPNotFound

class Plugin(object):

    name = None
    view_properties = []

    def __init__(self, view):
        self.view = view
        self.env = view.env
        setattr(view, self.name, self)
        for prop in self.view_properties:
            if hasattr(view, prop):
                value = getattr(view, prop)
                setattr(self, prop, value)
            assert hasattr(self, prop), \
                   'View name="%s": You must set "%s" property' % \
                                                        (self.view.name, prop)


class VP_Query(Plugin):

    name = 'query'

    view_properties = ['model', 'order_field', 'order_asc', 'limit']

    order_field = 'id'
    order_asc = True
    limit = 30

    @property
    def models(self):
        return self.view.env.models

    def get_model(self, name=None):
        return getattr(self.models, name or self.model)

    def get_order(self):
        field = getattr(self.get_model(), self.order_field)
        if self.order_asc:
            return field.asc()
        else:
            return field.desc()

    def create_query(self):
        return self.view.env.db.query(self.model)\

    def all(self):
        return self.query.order_by(self.get_order()).limit(self.limit).all()

    def get_or_404(self, **kwargs):
        obj = self.query.filter_by(**kwargs).first()
        if obj is None:
            raise HTTPNotFound()
        return obj

    @property
    def query(self):
        if hasattr(self.view.context, 'query'):
            return self.view.context.query
        else:
            query = self.create_query()
            self.query = query
            return query

    @query.setter
    def query(self, query):
        self.view.context.query = query


class VP_Response(Plugin):

    name = 'response'
    view_properties = ['templates_folder']

    @property
    def templates_folder(self):
        return self.view.name

    def template_name(self, template):
        folders = [self.templates_folder]
        parent = self.view.parent
        while parent:
            folders.insert(0, parent.response.templates_folder)
            parent = parent.parent
        return '%s/%s' % ('/'.join(folders), template)

    def template(self, template, kwargs):
        kwargs.setdefault('view', self.view)
        return self.view.env.render_to_response(self.template_name(template),
                                                kwargs)

