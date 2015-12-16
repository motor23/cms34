# -*- coding: utf-8 -*-
from datetime import timedelta
from webob.exc import HTTPNotFound
from iktomi.forms import widgets
from iktomi.cms.stream import FilterForm
from iktomi.cms.forms.fields import Field, FieldSet
from iktomi.unstable.forms import convs
from iktomi.utils import cached_property


class SearchForm(FilterForm):
    template = 'forms/search_form.html'

    def __init__(self, env, **kwargs):
        super(SearchForm, self).__init__(env, **kwargs)
        self.model = env.indices.Material

    @cached_property
    def search_options_model(self):
        return self.env.models.OptionsSearchFilters

    @cached_property
    def fields(self):
        return [
            Field('q', conv=convs.Char(),
                  widget=widgets.TextInput(template='search/query.html')),
            Field('filter',
                  conv=convs.ModelChoice(model=self.search_options_model),
                  widget=widgets.Select(template='search/filter_select.html',
                                        null_label=u'Все')),
            # FieldSet('dt', fields=[
            #     Field('since', conv=convs.Date(required=False)),
            #     Field('till', conv=convs.Date(required=False)),
            # ]),
        ]

    def filter_by__filter(self, query, field, value):
        """
        Filter sphinx query with attributes of SearchFilter.

        :param query: Sphinx query
        :param field: form field
        :param value: Instance of OptionsSearchFilters
        :return:
        """
        if value.type:
            query = query.filter_by(type=value.type)
        if value.section:
            query = query.filter_by(section_id=value.section_id)
        return query

    def filter_by__q(self, query, field, value):
        return query.match(value)

    def filter_by__dt(self, query, field, value):
        model = self.form.model
        since, till = value['since'], value['till']

        if since is not None:
            query = query.filter(getattr(model, field.name) >= since)
        if till is not None:
            next_day = till + timedelta(days=1)
            query = query.filter(getattr(model, field.name) < next_day)
        return query

    def render(self, **kwargs):
        return self.env.template.render(self.template, form=self, **kwargs)
