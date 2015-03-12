# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases
from iktomi.utils.paginator import ModelPaginator

from ....front.view import BaseView, view_handler
from ....front.plugins import VP_Query, VP_Response


class VP_OrgsQuery(VP_Query):
    model = 'Org'
    order = ('order', 'asc')
    limit = 50

    def create_query(self):
        return self.view.env.db.query(self.get_model())\
                            .filter_by(section_id=self.env.section.section.id)


class V_OrgsList(BaseView):
    name = 'orgs_list'
    title = u'Список организаций'

    plugins = [VP_OrgsQuery, VP_Response]

    @classmethod
    def cases(cls):
        return [
            match('/', name='index') | cls.h_index,
            match('/<int:item_id>/', name='item') | cls.h_item,
        ]

    @view_handler
    def h_index(self, env, data):
        orgs = self.query.all()
        return self.response.template('index', dict(orgs=orgs))

    @view_handler
    def h_item(self, env, data):
        org = self.query.get_or_404(id=data.item_id)
        if not org:
            raise HTTPNotFound()
        return self.response.template('item', dict(org=org))

    @classmethod
    def _url_for_index(cls, root):
        return root.index

    @classmethod
    def _url_for_obj(cls, root, obj):
        return root.item(item_id=obj.id)


h_orgs_list = V_OrgsList.handler()
