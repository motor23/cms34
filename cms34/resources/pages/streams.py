# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
)
from cms34.mixed.fields import (
    XB_Content,
    xf_title,
    xf_slug,
    xf_dt,
    xf_body,
)
from ..sections.fields import (
    xb_section_object,
)

class XB_Content(XB_Content):
    item_fields = [
        xf_body,
    ]

xb_content = XB_Content()


class SFY_Pages(StreamFactory):
    name = 'pages'
    model = 'Page'
    title = u'Страницы'
    limit = 40
    preview = True
    sort_initial_field = 'title'

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    item_fields = [
        xb_section_object,
        xb_content,
    ]
    list_fields = filter_fields = sort_fields = item_fields

