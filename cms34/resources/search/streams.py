# -*- coding: utf-8 -*-
from cms34.stream import StreamFactory
from cms34.resources.sections.fields import xb_section_object


class SFY_SearchSection(StreamFactory):
    name = 'search'
    model = 'SearchSection'
    title = u'Поиск'
    limit = 40
    preview = True
    sort_initial_field = 'id'

    permissions = {
        'wheel': 'rwxdcp',
        'editor': 'rwxdcp',
    }

    fields = sort_fields = filter_fields = item_fields = [
        xb_section_object,
    ]
