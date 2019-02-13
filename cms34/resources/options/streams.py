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
    label = u''
    sort_initial_field = 'order'
    list_fields = [
        xf_type,
    ]
    filter_fields = [
        xf_type,
    ]
    item_fields = [
        xf_type,
    ]
    sort_fields = [
        xb_object,
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
        'wheel': 'rwxdcp',
        'editor': 'rwxdcp',
    }

    item_form_factory = TypedItemFormFactory

    common_fields = [
        xb_main,
    ]
    sort_fields = filter_fields = list_fields = common_fields
    item_fields = {}
