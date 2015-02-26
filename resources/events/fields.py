# -*- coding: utf8 -*-
from cms34.mixed.fields import (
    XF_StreamSelect
)

class XF_Events(XF_StreamSelect):
    name = 'events'
    label = u'События'
    stream_name = 'events'
    model = 'Event'
    ordered = True
    multiple = True

xf_events = XF_Events()
