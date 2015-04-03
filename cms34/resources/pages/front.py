# -*- coding: utf-8 -*-
from iktomi.web import match

from ...front.view import view_handler
from .. import ResourceView
from ...front.plugins import VP_Response, VP_Query


class VP_PagesQuery(VP_Query):
    model = 'Page'
    order = ('order', 'asc')
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())


class V_Page(ResourceView):
    title = u'Страницы'
    name = 'page'

    plugins = [VP_Response, VP_PagesQuery]

    @classmethod
    def cases(cls, resources, section):
        return [
            match('/', name='index') | cls.h_index,
            resources.h_section(section),
        ]

    @view_handler
    def h_index(self, env, data):
        page = self.query.get_or_404(id=self.section.id)
        return self.response.template('index', dict(page=page))

