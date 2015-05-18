# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match
from iktomi.utils.paginator import ModelPaginator

from cms34.front.view import view_handler
from cms34.front.plugins import VP_Query, VP_Response

from .. import ResourceView


class VP_EventsQuery(VP_Query):
    model = 'Event'
    order = ('dt', 'desc')
    paginator_limit = 20

    @property
    def query(self):
        return self._query(self.env, section_id=self.view.section.id)

    @classmethod
    def _query(cls, env, section_id=None):
        query = cls._base_query(env)
        if section_id:
            query = query.filter_by(section_id=section_id)
        query = query.order_by(cls._get_order(env))
        if cls.limit:
            query = query.limit(cls.limit)
        return query


class V_EventsList(ResourceView):
    name = 'events_list'
    title = u'Лента событий'

    plugins = [VP_EventsQuery, VP_Response]
    paginator = ModelPaginator

    @classmethod
    def cases(cls, sections, section):
        return [
            match('/', name='index') | cls.h_index,
            match('/<int:item_id>/', name='item') | cls.h_item,
            sections.h_section(section),
        ]

    @view_handler
    def h_index(self, env, data):
        paginator = self.paginator(env.request, self.query.query,
                                limit=self.query.paginator_limit)
        return self.response.template('index',
                                      dict(paginator=paginator))

    @view_handler
    def h_item(self, env, data):
        event = self.query.get_or_404(id=data.item_id)
        if not event:
            raise HTTPNotFound()
        return self.response.template('item', dict(event=event))

    @classmethod
    def _url_for_obj(cls, root, obj):
        return root.item(item_id=obj.id)
