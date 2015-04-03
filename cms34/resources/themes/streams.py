# -*- coding: utf8 -*-

from ...stream import (
    StreamFactory,
)
from ...mixed.fields import (
    XF_Block,
    xf_lead,
    xb_object,
)


class XB_Main(XF_Block):
    name = 'sections_block'
    label = u'Тема'
    list_fields = [
        xf_lead,
    ]
    sort_fields = [
    ]
    filter_fields = [
    ]
    item_fields = [
        xf_lead,
    ]

xb_main = XB_Main()


class ThemesStreamFactory(StreamFactory):
    name = 'themes'
    model = 'Theme'
    title = u'Тема'
    limit = 40

    blocks = [
        xb_object,
        xb_main,
    ]
    list_fields = sort_fields = filter_fields = item_fields = blocks

