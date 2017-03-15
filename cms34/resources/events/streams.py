# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
)
from cms34.mixed import (
    XF_StreamSelect,
    XB_Content,
    xf_title,
    xf_lead,
    xf_dt,
    xf_publish_dt,
    xf_body,
    xb_object,
)
from cms34.resources.sections.blocks import xb_section


class XB_Content(XB_Content):
    list_fields = [
        xf_title,
        xf_dt,
        xf_publish_dt,
    ]
    sort_fields = filter_fields = list_fields
    item_fields = [
        xf_dt,
        xf_publish_dt,
        xf_title,
        xf_lead,
        xf_body,
    ]

xb_content = XB_Content()


class SFY_Events(StreamFactory):
    name = 'events'
    model = 'Event'
    title = u'События'
    limit = 40
    sort_initial_field = '-dt'
    obj_endpoint = True

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    fields = [
        xb_object,
        xb_content,
        xb_section,
    ]
    list_fields = sort_fields = filter_fields = item_fields = fields

