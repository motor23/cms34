from iktomi.web import WebHandler, cases, prefix
from ..front.view import BaseView, HView

class H_Resources(WebHandler):

    _sections = {}
    _handler = None

    def __init__(self, resources):
        self.resources = resources
        self.cached_db = self.resources.app.cached_db_maker()

    def _locations(self):
        return self.handler()._locations()

    def __call__(self, env, data):
        return self.handler().__call__(env, data)

    @property
    def _next_handler(self):
        return self.handler()._next_handler()

    def __or__(self, next_handler):
        raise AttributeError('__or__ is not allowed for H_resources handler')

    def handler(self):
        if self.rebuild_sections_dict():
            self._handler = self.resources.h_section()
        return self._handler

    def rebuild_sections_dict(self):
        section_items = self.cached_db.query(self.resources.model).all()
        sections = dict([(section.id, section.tree_path) \
                                              for section in section_items])
        if sections == self._sections:
            return False
        else:
            self._sections = sections
            return True


def H_Section(resources, section=None):
    parent_id = section and section.id or None
    subsections = resources.cached_db.query(resources.model)\
                                     .filter_by(parent_id=parent_id).all()
    handlers = []
    for subsection in subsections:
        resource = resources.get_resource(subsection.type)
        if not resource:
            print subsection.type
            continue
        handler = resource.handler(resources, subsection)
        handler = prefix('/' + subsection.slug, name=subsection.slug) | handler
        handlers.append(handler)
    return cases(*handlers)


class Resources(object):

    def __init__(self, app, model, resources=[]):
        self.app = app
        self.resources = resources
        self.resources_dict = dict([(res.name, res) for res in resources])
        self.cached_db = app.cached_db_maker()
        self.model = model

    def h_resources(self):
        return H_Resources(self)

    def h_section(self, section=None):
        return H_Section(self, section)

    def get_resource(self, name):
        res = self.resources_dict.get(name)
        return res
        assert res is not None, 'Unknown resource, name="%s"' % name
        return res

    def url_for_obj(self, root, obj):
        if isinstance(obj, self.model):
            return self.url_for_section(root, obj)
        if hasattr(obj, 'section'):
            section_root = self.root_for_section(root, section)
            url = self.get_resource(section.type).view_cls\
                                             ._url_for_obj(section_root, obj)
            if url:
                return url
        return None

    def root_for_section(self, root, section):
        slugs = [section.slug] + [p.slug for p in section.parents]
        slugs.reverse()
        return root.build_subreverse('.'.join(slugs))

    def url_for_section(self, root, section):
        try:
            section_root = self.root_for_section(root, section)
            url = self.get_resource(section.type).view_cls\
                                             ._url_for_index(section_root)
        except Exception, exc:
            raise
            raise Exception(exc)
        if url:
            return url
        else:
            sections = self.get_sections(parent_id=section.id)
            if sections:
                return self.url_for_section(root, sections[0])
            else:
                return None

    def get_sections(self, **kwargs):
        return self.cached_db.query(self.model)\
                             .filter_by(**kwargs).all()


class ResourceBase(object):

    name = None
    view_cls = None

    def __init__(self, name=None):
        self.name = name or self.name
        assert self.name

    def handler(self, resources, section=None):
        return self.view_cls.handler(resources, section)


class ResourceView(BaseView):

    def __init__(self, env, cls, section=None):
        self.section = section
        BaseView.__init__(self, env, cls)

    @classmethod
    def cases(cls, resources, section):
        return []

    @classmethod
    def handler(cls, resources, section):
        return HView(cls, section=section) | \
               cases(*cls.cases(resources, section))

    def breadcrumbs(self, children=[]):
        crumbs = [(self.section, self.section.title)] + children
        if self.parent:
            return self.parent.breadcrumbs(crumbs)
        return crumbs

    @classmethod
    def _url_for_index(cls, root):
        return root.index

