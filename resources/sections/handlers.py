# -*- coding:utf8 -*-
from webob.exc import HTTPNotFound

from iktomi.web import WebHandler, cases, namespace, prefix, UrlBuildingError
from iktomi.utils import cached_property

from common.handlers.context import BaseContext, HContext


class SectionBuilder(object):
    def __init__(self, name, get_sections):
        self.name = name
        self.arg_name = '%s_path' % name
        self._url_params = {self.name: None,
                            self.arg_name: None}
        self.get_sections = get_sections

    def match(self, path, env, **kw):
        for section in self.get_sections(env):
            if path.startswith(section.tree_path):
                return section.tree_path, \
                       {self.arg_name: path, self.name: section}
        else:
            return None, None

    def __call__(self, **kwargs):
        section = kwargs.get(self.name)
        value = section and section.tree_path or kwargs.get(self.arg_name)
        if value is None:
            raise UrlBuildingError(
                        'Missing argument for '
                        'URL builder: %s or %s' % (self.name, self.arg_name))
        return value

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.name)


class HSectionPrefix(prefix):

    def __init__(self, name, get_sections):
        self.builder = SectionBuilder(name, get_sections)
        self._next_handler = namespace(name)


class HSectionResources(WebHandler):

    def __init__(self, name, resources):
        self.name = name
        self.handlers = dict([(res.name, namespace(res.name) | res.handler())
                                     for res in resources])
        self._next_handler = cases(*self.handlers.values())

    def section_resources(self, env, data):
        if not data.section.type:
            raise HTTPNotFound()
        if data.section.type == '404':
            raise HTTPNotFound()
        return self.handlers[data.section.type](env, data)
    __call__ = section_resources


class SectionContext(BaseContext):
    def __init__(self, env, data):
        BaseContext.__init__(self, env, data)
        self.section = data.section

    @cached_property
    def sections_list(self):
        result = []
        section = self.section
        while section:
            result.append(section)
            section = self.get_cached_section(section.parent_id)
        result.reverse()
        return result

    def get_cached_section(self, section_id):
        if not section_id:
            return None
        return self.env.cached_db.query(self.env.models.Section)\
                                 .filter_by(id=section_id)\
                                 .order_by('order').first()



def get_sections(env):
    return env.cached_db.query(env.models.Section)\
              .order_by('tree_path', 'desc').all()


def HSection(name='section',
             get_sections=get_sections,
             resources=[],
             context_cls=SectionContext):
    return HSectionPrefix(name, get_sections) | \
           HContext(name, context_cls) | \
           HSectionResources(name, resources)

