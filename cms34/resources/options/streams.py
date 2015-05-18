# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
    TypedItemFormFactory,
    SFP_ImageUpload,
)

from cms34.mixed import (
    XF_Block,
    xb_object,
    xf_title,
    xf_order,
    xf_publish_dt,
    xf_type,
)


class XB_Main(XF_Block):
    name = 'media_block'
    label = u'Медия'
    initial_sort = 'order'
    list_fields = [
        xf_title,
        xf_order,
    ]
    filter_fields = [
        xf_type,
        xf_title,
    ]
    item_fields = [
        xf_type,
        xf_title,
        xf_order,
    ]
    sort_fields = [
       xf_title,
       xf_order,
    ]

xb_main = XB_Main()


class SFY_Options(StreamFactory):
    name = 'options'
    model = 'Options'
    title = u'Опции'
    limit = 40
    preview = True
    plugins = [SFP_ImageUpload]

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    item_form_factory = TypedItemFormFactory

    common_fields = [
        xb_object,
        xb_main,
    ]
    sort_fields = filter_fields = list_fields = common_fields
    item_fields = {}


