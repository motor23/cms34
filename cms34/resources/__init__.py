import logging
import copy
from webob.exc import HTTPNotFound
from iktomi.web import WebHandler, cases, prefix, UrlBuildingError
from sqlalchemy.ext.serializer import dumps, loads
from sqlalchemy.sql import func

from ..front.view import BaseView, HView

logger = logging.getLogger()


class BindedSections(object):

    def __init__(self, sections, db, cache=None, cache_timeout=60):
        self.sections = sections
        self.db = db
        self.cache = cache
        self.cache_timeout = cache_timeout

    def update(self):
        version = self.get_version_from_cache()
        if version is not None:
            if version==self.sections.version:
                return False
            else:
                items = self.get_from_cache()
        else:
            items = None

        if items is None:
            version = self.get_version_from_db()
            if version==self.sections.version:
                return False
            else:
                items = self.get_from_db()
            self.set_to_cache(version, items)
        self.sections.set_sections(version, items)
        return True

    def get_from_db(self):
        items = self.db.query(self.sections.model) \
            .with_polymorphic('*') \
            .order_by(self.sections.model.order).all()
        items = self.filter_items_from_db(items)
        map(lambda x: self.db.expunge(x), items)
        return items

    def get_version_from_db(self):
        model = self.sections.model
        cnt = self.db.query(model.id).count()
        updated_dt = self.db.query(func.max(model.updated_dt)).first()
        return (updated_dt, cnt)

    def filter_items_from_db(self, items):
        # remove items with unpublished parents
        parents = dict([(item.parent_id, item) for item in items])
        parent_ids = [None]
        result = []
        while parent_ids:
            new_parent_ids = []
            for item in items:
                if item.parent_id in parent_ids:
                    result.append(item)
                    new_parent_ids.append(item.id)
            parent_ids = new_parent_ids
        items = result

        # remove sections with double (slugs, parant_id) pairs 
        # filter not published sections
        result = []
        pairs = []
        for item in items:
            pair = (item.slug, item.parent_id)
            if pair not in pairs:
                pairs.append(pair)
                result.append(item)
        return result

    def get_from_cache(self):
        if self.cache:
            items = self.cache.get(self.sections.data_cache_key)
            if items is not None:
                return loads(items)

    def get_version_from_cache(self):
        if self.cache:
            return self.cache.get(self.sections.version_cache_key)
        else:
            return None

    def set_to_cache(self, version, items):
        if self.cache:
            self.cache.set(self.sections.data_cache_key, dumps(items),
                           time=self.cache_timeout)
            self.cache.set(self.sections.version_cache_key, version,
                           time=self.cache_timeout)

    def merge_item(self, item):
        return self.db.merge(item, load=False)

    def get_sections(self, **kwargs):
        items = self.sections.get_sections(**kwargs)
        return map(lambda x: self.merge_item(x), items)

    def get_section(self, **kwargs):
        section = self.sections.get_section(**kwargs)
        if section is not None:
            return self.merge_item(section)
        else:
            return None

    def get(self, id, default=None):
        section = self.sections.get(id, default)
        if section is not None:
            return self.merge_item(section)
        else:
            return None

    def url_for_obj(self, root, obj, default=None):
        return self.sections.url_for_obj(root, obj, default=default)

    def url_for_section(self, root, section):
        return self.sections.url_for_section(root, section)

    def root_for_section(self, root, section):
        return self.sections.root_for_section(root, section)


class V_Sections(object):

    binded_class = BindedSections

    def __init__(self, model, resources, db=None, cache=None):
        self.model = model
        self.data_cache_key = "data-%s" % model.__name__
        self.version_cache_key = "version-%s" % model.__name__
        self.version = None
        self.resources = resources
        self.db = db
        self.cache = cache
        self.get_sections_cache = {}
        self.sections = []
        self.sections_dict = {}
        self.sections_by_parent = {}

    def bind(self, db, cache):
        return self.binded_class(self, db, cache)

    def set_sections(self, version, sections):
        self.sections = map(lambda x: copy.copy(x), sections)
        self.sections_dict = dict([(s.id, s) for s in self.sections])
        self.sections_by_parent = {}
        for section in self.sections:
            self.sections_by_parent.setdefault(section.parent_id, [])\
                                   .append(section)
        self.version = version
        self.get_sections_cache = {}

    def get(self, id, default=None):
        if id in self:
            return self[id]
        else:
            return default

    def __getitem__(self, key):
        return self.sections_dict[key]

    def __iter__(self):
        return self.sections_dict.__iter__()

    def get_sections(self, **kwargs):
        result = []
        cache_key = str(kwargs)
        # Try cache
        if self.get_sections_cache.has_key(cache_key):
            return self.get_sections_cache[cache_key]
        # Try indexes
        if kwargs.has_key('id'):
            section = self.get(kwargs.pop('id'))
            sections = section and [section] or []
        elif kwargs.has_key('parent_id'):
            sections = self.sections_by_parent.get(kwargs.pop('parent_id'), [])
        else:
            sections = self.sections
        for section in sections:
            for key, value in kwargs.items():
                if value != getattr(section, key):
                    break
            else:
                result.append(section)
        self.get_sections_cache[cache_key] = result
        return result

    def get_section(self, **kwargs):
        sections = self.get_sections(**kwargs)
        return sections and sections[0] or None

    def handler(self):
        return self.h_section()

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

    # XXXX
    def get_section_parents(self, section):
        result = []
        if section.parent_id is None:
            return result
        parent_id = section.parent_id
        while parent_id:
            parent = self.get_section(id=parent_id)
            if not parent:  # parent not published
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
            url = self.resources.get_resource(obj.section.type).view_cls \
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
        url = self.resources.get_resource(section.type).view_cls \
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


class ResourceView(BaseView):
    def __init__(self, env, cls, section):
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

