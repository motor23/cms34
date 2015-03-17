# -*- coding: utf-8 -*-
from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError


class Show(Extension):
    allowed_languages = ['ru', 'en']

    tags = set(['show'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        token = next(parser.stream)

        if token.value not in self.allowed_languages:
            raise TemplateSyntaxError('Expected language token from set: %s' %
                                      ', '.join(self.allowed_languages), lineno)

        body = parser.parse_statements(['name:endshow'], drop_needle=True)
        node = nodes.CallBlock(self.call_method('_show_support', [nodes.Const(token.value)]),
            [], [], body).set_lineno(lineno)
        return node

    def _show_support(self, lang, timeout=None, caller=None):
        if self.environment.globals['env'].lang == lang:
            return caller()
        return u''
