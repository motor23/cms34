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
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())\
                            .filter_by(section_id=self.view.section.id)


class V_EventsList(ResourceView):
    name = 'events_list'
    title = u'Лента событий'

    plugins = [VP_EventsQuery, VP_Response]
    paginator = ModelPaginator

    @classmethod
    def cases(cls, resources, section):
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


    def _url_for_obj(self, root, obj):
        if isinstance(obj, self.query.get_model()):
            return root.item(item_id=obj.id)
