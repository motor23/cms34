# -*- coding: utf-8 -*-
import logging
from webob.exc import HTTPNotFound
from iktomi.utils import cached_property
from iktomi.utils.paginator import ModelPaginator
from cms34.front import VP_Response, view_handler
from cms34.resources import ResourceView
from cms34.apps.common.guarded_urls import GuardedMatch
from cms34.apps.common.handlers import no_preview
from .forms import SearchForm

logger = logging.getLogger('')


class EmptyQuery(object):
    count = lambda self: 0
    __iter__ = lambda self: []


class SphinxPaginator(ModelPaginator):
    limit = 20

    def __init__(self, env, request, sphinx_query, **kwargs):
        self._env = env
        super(SphinxPaginator, self).__init__(request, sphinx_query, **kwargs)

    @cached_property
    def items(self):
        sphinx_items = self.slice(self._query)
        items = []
        for item in sphinx_items:
            try:
                item_model = getattr(self._env._models, item.model_name)
            except AttributeError:
                logger.warning(
                    'Wrong model identity for item in Sphinx collection: <%s>, '
                    'item ID = %s. Item will be skipped in search feed.',
                    item.model_name, item.document_id)
            else:
                real_item = self._env.db.query(item_model).get(item.document_id)
                items.append(real_item)

        return items


class V_Search(ResourceView):
    name = 'search'

    index_params = {
        'q': unicode,
        'filter': int,
    }

    plugins = [VP_Response]

    @classmethod
    def cases(cls, sections, section):
        return [
            GuardedMatch('/', name='index',
                         params=cls.index_params) | no_preview | cls.h_index,
            sections.h_section(section)
        ]

    @view_handler
    def h_index(self, env, data):
        data.form = frm = SearchForm(env)

        Material = env.indices.Material
        sphinx_query = env.sphinx.query(Material)
        frm.accept(env.request.GET)
        if frm.is_valid:
            if data.form.python_data['q']:
                sphinx_query = data.form.filter(sphinx_query)
            else:
                sphinx_query = EmptyQuery()
        else:
            raise HTTPNotFound()

        data.paginator = SphinxPaginator(env, env.request, sphinx_query)

        return self.response.template('index', data.as_dict())
