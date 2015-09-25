# -*- coding: utf-8 -*-
from iktomi.web import match

from ...front.view import view_handler
from .. import ResourceView
from ...front.plugins import VP_Response, VP_Query


class VP_PagesQuery(VP_Query):
    model = 'Page'
    order_field = 'order'
    order_asc = True
    limit = 20


class V_Page(ResourceView):
    title = u'Страницы'
    name = 'page'

    plugins = [VP_Response, VP_PagesQuery]

    @classmethod
    def cases(cls, sections, section):
        return [
            match('/', name='index') | cls.h_index,
            sections.h_section(section),
        ]

    @view_handler
    def h_index(self, env, data):
        return self.response.template('index', dict())

