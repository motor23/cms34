# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases
from iktomi.utils.paginator import ModelPaginator

from common.handlers.context import BaseContext, HContext
from std.model.factories import ModelFactory

name = 'events_list'
title = u'Лента событий'

def index(env, data):
    query = env.resource.query()
    paginator = env.resource.paginator(env.request, query,
                                       limit=env.resource.limit)
    return env.resource.render_to_response('index', dict(paginator=paginator))

def item(env, data):
    event = env.resource.query().filter_by(id=data.item_id).first()
    if not event:
        raise HTTPNotFound()
    return env.resource.render_to_response('item', dict(event=event))


h_index = match('/', name='index') | index
h_item = match('/<int:item_id>/', name='item') | item


def url_for_index(root):
    return root.index


def url_for_obj(root, obj):
    return root.item(item_id=obj.id).as_url


class Context(BaseContext):

    name = name
    model_name = 'Event'
    limit = 20
    paginator = ModelPaginator
    cases = [h_index, h_item]

    def url_for_item(self, obj):
        return url_for_obj(self.root, obj)

    def model(self):
        return getattr(self.env.models, self.model_name)

    def query(self):
        return self.env.db.query(self.model())\
                       .filter_by(section_id=self.env.section.section.id)\
                       .order_by(self.model().dt.desc())

    @classmethod
    def handler(cls):
        return HContext('resource', cls) | cases(*cls.cases)


handler = Context.handler()


class EventsListSection(ModelFactory):
    title = title
