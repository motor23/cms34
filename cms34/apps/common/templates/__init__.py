import os
import jinja2
import jinja2.filters
import urlparse
import urllib
from webob.response import Response

from .filters import all_filters
from .functions import all_functions
from .macros import MacrosLib
from .tags import Show
from .cache import BlockCacheExtension


class TemplateEngine(object):

    default_extension = 'html'
    filters = {}
    globals = {}
    extensions = []
    autoescape=True,

    def __init__(self, paths, **kwargs):
        self.__dict__.update(kwargs)

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(paths),
            autoescape=self.autoescape,
            extensions=self.extensions)
        self.env.filters.update(self.filters)
        self.env.install_null_translations()
        self.env.globals.update(self.globals)

    def resolve(self, name):
        base, ext = os.path.splitext(name)
        if not ext:
            return '.'.join((base, self.default_extension))
        return name

    def render(self, name, **vars):
        name = self.resolve(name)
        return jinja2.Markup(self.env.get_template(name).render(**vars))

    def render_to_string(self, name, vars={}, **kwargs):
        vars = dict(vars, **kwargs) #XXX
        return self.render(name, **vars)

    def render_to_response(self, name, vars, content_type='text/html'):
        result = self.render(name, **vars)
        return Response(result, content_type=content_type)


class AppTemplateEngine(TemplateEngine):

    extensions = ['jinja2.ext.i18n', Show, BlockCacheExtension]

    filters = {}
    filters.update(all_filters)

    globals = {}
    globals.update(all_functions)

    def __init__(self, paths, **kwargs):
        TemplateEngine.__init__(self, paths, **kwargs)
        self.env.globals.update({
            'macros': MacrosLib(self),
        })

