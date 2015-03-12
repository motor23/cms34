# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
)
from ...mixed.fields import (
    XF_Block,
    xf_title,
    xf_lead,
    xf_dt,
    xf_publish_dt,
    xf_body,
    XF_StreamSelect,
    xb_object,
)

class XB_Main(XF_Block):
    name = 'event_block'
    label = u'Материал'
    list_fields = [
        xf_title,
        xf_lead,
        xf_dt,
        xf_publish_dt,
    ]
    sort_fields = [
        xf_dt,
        xf_publish_dt,
    ]
    filter_fields = [
        xf_title,
        xf_dt,
        xf_publish_dt,
    ]
    item_fields = [
        xf_dt,
        xf_publish_dt,
        xf_title,
        xf_lead,
        xf_body,
    ]

xb_main = XB_Main()

class EventsStreamFactory(StreamFactory):
    name = 'events'
    model = 'Event'
    title = u'События'
    limit = 40

    blocks = [
        xb_object,
        xb_main,
    ]
    list_fields = sort_fields = filter_fields = item_fields = blocks

