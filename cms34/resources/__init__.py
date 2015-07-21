import logging
from webob.exc import HTTPNotFound
from iktomi.web import WebHandler, cases, prefix, UrlBuildingError
from ..front.view import BaseView, HView

logger = logging.getLogger()

class V_Sections(object):
    def __init__(self, db, cached_db, model, resources):
        self.db = db
        self.cached_db = cached_db
        self.model = model
        self.resources = resources
        self.sections_query = None

    def handler(self):
        return H_Sections(self)

    def h_section(self, section=None):
        parent_id = section and section.id or None
        subsections = self.get_sections(parent_id=parent_id)
        handlers = []
        for subsection in subsections:
            resource = self.resources.get_resource(subsection.type)
            handler = resource.handler(self, subsection)
            handler = prefix('/' + (subsection.slug or ''),
                             name=subsection.slug) | handler
            handlers.append(handler)
        return cases(*handlers)

    def load_sections(self):
        _query = self.db.query(self.model)\
                        .with_polymorphic('*')\
                        .order_by(self.model.order)
        self.sections_query = self.cached_db.query(self.model, _query,
                                                   reload=True)


    def get_sections(self, reload=False, **kwargs):
        result = []
        if self.sections_query is None or reload:
            self.load_sections()
        sections = self.sections_query.filter_by(**kwargs).all()
        #remove sections with double (slugs, parant_id) pairs 
        # filter not published sections
        pairs = []
        for section in sections:
            pair = (section.slug, section.parent_id)
            if pair not in pairs:
                pairs.append(pair)
                if self.get_section_parents(section) is not None:
                    result.append(section)
        return result

    def retrieve_sections(self, **kwargs):
        ids = map(lambda x: x.id, self.get_sections(**kwargs))
        return self.db.query(self.model).filter(self.model.id.in_(ids)).all()

    def get_section(self, **kwargs):
        sections = self.get_sections(**kwargs)
        return sections and sections[0] or None

    def get(self, id, default=None):
        return self.get_section(id=id) or default

    def get_section_parents(self, section):
        result = []
        if section.parent_id is None:
            return result
        parent_id = section.parent_id
        while parent_id:
            parent = self.get_section(id=parent_id)
            if not parent: # parent not published
                return None
            result.append(parent)
            parent_id = parent.parent_id
        return result

    def url_for_obj(self, root, obj, default=None):
        if isinstance(obj, self.model):
            return self.url_for_section(root, obj)
        if hasattr(obj, 'section') and obj.section:
            section_root = self.root_for_section(root, obj.section)
            if not section_root:
                return default
            url = self.resources.get_resource(obj.section.type).view_cls\
                                ._url_for_obj(section_root, obj)
            if url:
                return url
        return default

    def root_for_section(self, root, section):
        parents = self.get_section_parents(section)
        if parents is None:
            return None
        slugs = [section.slug] + [p.slug for p in parents]
        slugs.reverse()
        try:
            return root.build_subreverse('.'.join(slugs))
        except UrlBuildingError:
            return None

    def url_for_section(self, root, section):
        section_root = self.root_for_section(root, section)
        if not section_root:
            return None
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

    def __del__(self):
        logger.debug('__del__: %s' % self)


class H_Sections(WebHandler):

    _sections = {}
    _handler = cases()

    def __init__(self, sections):
        self.sections = sections

    def _locations(self):
        return self.handler()._locations()

    def __call__(self, env, data):
        #env.sections = self.sections
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
        section_items = self.sections.get_sections(reload=True)
        self.sections.db.close()
        sections = [(section.id, self.tree_path(section)) \
                                              for section in section_items]
        sections = dict(filter(lambda x: x[1], sections))
        if sections == self._sections:
            return False
        else:
            self._sections = sections
            return True

    def tree_path(self, section):
        # default tree_path raise Exception when get relation
        parents = self.sections.get_section_parents(section)
        if parents is None:
            return None
        slugs = [section.slug] + [item.slug for item in parents]
        slugs.reverse()
        slugs = map(lambda x: x or '', slugs)
        return '/' + '/'.join(slugs) + '/'



class ResourceView(BaseView):

    def __init__(self, env, cls, section=None):
        self.section = env.sections.get(section.id)
        if self.section:
            env.section = self.section
        else:
            raise HTTPNotFound
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

    def create_streams(self, register, names=None, **kwargs):
        if not names or self.sections_stream_factory.name in names:
            self.sections_stream_factory(register, self.resources, **kwargs)
        for f in self.stream_factories:
            if not names or f.name in names:
                f(register, **kwargs)

    def register_models(self, register, names=None, **kwargs):
        for f in self.model_factories:
            if not names or f.name in names:
                f(register, **kwargs)
        if not names or self.sections_model_factory.name in names:
            self.sections_model_factory(register, self.resources, **kwargs)

