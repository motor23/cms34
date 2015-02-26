# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases

from ....front.view import BaseView, view_handler
from ....front.plugins import VP_Query, VP_Response


class VP_PagesQuery(VP_Query):
    model = 'Page'
    order = ('order', 'asc')
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())\
                            .filter_by(section_id=self.env.section.section.id)


class V_Pages(BaseView):
    title = u'Страницы'
    name = 'pages'

    plugins = [VP_PagesQuery, VP_Response]

    @classmethod
    def cases(cls):
        return [
            match('/', name='index') | cls.h_index,
            match('/<string:slug>/', name='internal') | cls.h_internal,
        ]

    @view_handler
    def h_index(self, env, data):
        page = self.query.get_or_404(slug='')
        if not page:
            raise HTTPNotFound()
        return self.response.template('page', dict(page=page))

    @view_handler
    def h_internal(self, env, data):
        page = self.query.get_or_404(slug=data.slug)
        if not page:
            raise HTTPNotFound()
        return self.response.template('page', dict(page=page))

    @classmethod
    def _url_for_index(cls, root):
        return root.index

    @classmethod
    def _url_for_obj(cls, root, obj):
        if hasattr(obj, 'slug'):
            return root.internal(slug=obj.slug)
        else:
            return cls._url_for_index(root)


h_pages = V_Pages.handler()
