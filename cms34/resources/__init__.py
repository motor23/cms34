from iktomi.web import WebHandler, cases, prefix
from ..front.view import BaseView, HView


class V_Sections(object):
    def __init__(self, cached_db, models, resources):
        self.cached_db = cached_db
        self.model = getattr(models, resources.sections_model_factory.model)
        self.resources = resources

    def handler(self):
        return H_Sections(self)

    def h_section(self, section=None):
        parent_id = section and section.id or None
        subsections = self.get_sections(parent_id=parent_id)
        handlers = []
        for subsection in subsections:
            resource = self.resources.get_resource(subsection.type)
            handler = resource.handler(self, subsection)
            handler = prefix('/' + subsection.slug, name=subsection.slug) | \
                      handler
            handlers.append(handler)
        return cases(*handlers)

    def get_sections(self, **kwargs):
        return self.cached_db.query(self.model)\
                             .filter_by(**kwargs).all()

    def url_for_obj(self, root, obj):
        if isinstance(obj, self.model):
            return self.url_for_section(root, obj)
        if hasattr(obj, 'section'):
            section_root = self.root_for_section(root, section)
            url = self.resources.get_resource(section.type).view_cls\
                                ._url_for_obj(section_root, obj)
            if url:
                return url
        return None

    def root_for_section(self, root, section):
        slugs = [section.slug] + [p.slug for p in section.parents]
        slugs.reverse()
        return root.build_subreverse('.'.join(slugs))

    def url_for_section(self, root, section):
        section_root = self.root_for_section(root, section)
        url = self.resources.get_resource(section.type).view_cls\
                            ._url_for_index(section_root)
        if url:
            return url
        else:
            sections = self.get_sections(parent_id=section.id)
            if sections:
                return self.url_for_section(root, sections[0])
            else:
                return None


class H_Sections(WebHandler):

    _sections = {}
    _handler = cases()

    def __init__(self, sections):
        self.sections = sections

    def _locations(self):
        return self.handler()._locations()

    def __call__(self, env, data):
        env.sections = self.sections
        return self.handler().__call__(env, data)

    @property
    def _next_handler(self):
        return self.handler()._next_handler()

    def __or__(self, next_handler):
        raise AttributeError('__or__ is not allowed for H_resources handler')

    def handler(self):
        if self.rebuild_sections_dict():
            self._handler = self.sections.h_section()
        return self._handler

    def rebuild_sections_dict(self):
        section_items = self.sections.get_sections()
        sections = dict([(section.id, section.tree_path) \
                                              for section in section_items])
        if sections == self._sections:
            return False
        else:
            self._sections = sections
            return True


class ResourceView(BaseView):

    def __init__(self, env, cls, section=None):
        self.section = section
        BaseView.__init__(self, env, cls)

    @classmethod
    def cases(cls, sections, section):
        return []

    @classmethod
    def handler(cls, sections, section):
        return HView(cls, section=section) | \
               cases(*cls.cases(sections, section))

    def breadcrumbs(self, children=[]):
        crumbs = [(self.section, self.section.title)] + children
        if self.parent:
            return self.parent.breadcrumbs(crumbs)
        return crumbs

    @classmethod
    def _url_for_index(cls, root):
        return root.index


class ResourceBase(object):

    name = None
    view_cls = None
    section_model_factory = None
    section_stream_item_fields = None
    model_factories = []
    stream_factories = []

    def __init__(self, name=None):
        self.name = name or self.name
        assert self.name

    def handler(self, sections, section=None):
        return self.view_cls.handler(sections, section)


class ResourcesBase(object):

    model_factories = []
    stream_factories = []
    sections_model_factory = None
    sections_stream_factory = None

    def __init__(self, resources=[]):
        self.resources = resources
        self.resources_dict = dict([(res.name, res) for res in resources])
        model_factories = []
        for res in self.resources:
            model_factories += res.model_factories
        self.model_factories = model_factories
        stream_factories = []
        for res in self.resources:
            stream_factories += res.stream_factories
        self.stream_factories = stream_factories

    def get_resource(self, name):
        res = self.resources_dict.get(name)
        assert res is not None, 'Unknown resource, name="%s"' % name
        return res

    def create_streams(self, register, **kwargs):
        self.sections_stream_factory(register, self.resources, **kwargs)
        for f in self.stream_factories:
            f(register, **kwargs)

    def register_models(self, register, **kwargs):
        for f in self.model_factories:
            f(register, **kwargs)
        self.sections_model_factory(register, self.resources, **kwargs)

