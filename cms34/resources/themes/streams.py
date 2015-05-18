# -*- coding: utf8 -*-

from cms34.stream import (
    StreamFactory,
)
from cms34.mixed.fields import (
    XB_Content,
    xf_lead,
)
from ..sections.fields import (
    xb_section_object
)


class XB_Content(XB_Content):
    list_fields = [
        xf_lead,
    ]
    item_fields = [
        xf_lead,
    ]

xb_content = XB_Content()


class SFY_Themes(StreamFactory):
    name = 'themes'
    model = 'Theme'
    title = u'Темы'
    limit = 40
    sort_initial_field = 'title'

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    fields = [
        xb_section_object,
        xb_content,
    ]
    list_fields = sort_fields = filter_fields = item_fields = fields

