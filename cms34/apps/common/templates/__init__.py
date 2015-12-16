import os
import jinja2
import jinja2.filters
import urlparse
import urllib
from webob.response import Response
from iktomi.templates import BoundTemplate as BoundTemplateBase

from .filters import all_filters
from .functions import all_functions
from .tags import Show, Preview
from .cache import BlockCacheExtension


class TemplateEngine(object):

    default_extension = 'html'
    filters = {}
    globals = {}
    extensions = []
    autoescape=True,

    def __init__(self, app, paths, **kwargs):
        self.app = app
        self.__dict__.update(kwargs)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(paths),
            autoescape=self.autoescape,
            extensions=self.extensions)
        self.env.filters.update(self.filters)
        self.env.install_null_translations()
        self.env.globals.update(self.globals)
        self.env.globals['app'] = self.app

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

    extensions = ['jinja2.ext.i18n', Show, BlockCacheExtension, Preview]

    filters = {}
    filters.update(all_filters)

    globals = {}
    globals.update(all_functions)


class BoundTemplate(BoundTemplateBase):

    def get_template_vars(self):
        return self.env.get_template_vars()
