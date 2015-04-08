# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
)
from ...mixed.fields import (
    XF_Block,
    xb_object,
    xf_title,
    xf_slug,
    xf_dt,
    xf_body,
)

class XB_Main(XF_Block):
    name = 'page_block'
    label = u'Страница'
    list_fields = [
        xf_title,
        xf_slug,
    ]
    sort_fields = [
        xf_slug,
    ]
    filter_fields = [
        xf_title,
        xf_slug,
    ]
    item_fields = [
        xf_slug,
        xf_title,
        xf_body,
    ]

xb_main = XB_Main()


class PagesStreamFactory(StreamFactory):
    name = 'pages'
    model = 'Page'
    title = u'Страницы'
    limit = 40
    preview = True

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    blocks = [
        xb_object,
        xb_main,
    ]
    list_fields = sort_fields = filter_fields = item_fields = blocks


