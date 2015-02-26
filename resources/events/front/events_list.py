# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases
from iktomi.utils.paginator import ModelPaginator

from ....front.view import BaseView, view_handler
from ....front.plugins import VP_Query, VP_Response


class VP_EventsQuery(VP_Query):
    model = 'Event'
    order = ('dt', 'desc')
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())\
                            .filter_by(section_id=self.env.section.section.id)


class V_EventsList(BaseView):
    name = 'events_list'
    title = u'Лента событий'

    plugins = [VP_EventsQuery, VP_Response]
    paginator = ModelPaginator

    @classmethod
    def cases(cls):
        return [
            match('/', name='index') | cls.h_index,
            match('/<int:item_id>/', name='item') | cls.h_item,
        ]

    @view_handler
    def h_index(self, env, data):
        paginator = self.paginator(env.request, self.query.query,
                                limit=self.query.limit)
        return self.response.template('index',
                                      dict(paginator=paginator))

    @view_handler
    def h_item(self, env, data):
        event = self.query.get_or_404(id=data.item_id)
        if not event:
            raise HTTPNotFound()
        return self.response.template('item', dict(event=event))


    @classmethod
    def _url_for_index(cls, root):
        return root.index

    @classmethod
    def _url_for_obj(cls, root, obj):
        return root.item(item_id=obj.id)


h_events_list = V_EventsList.handler()

