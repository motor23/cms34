# -*- coding: utf8 -*-

from ...mixed import (
    XF_StreamSelect,
)

class XF_Section(XF_StreamSelect):
    name = 'section'
    label = u'Раздел'
    model = 'Section'
    stream_name = 'sections'


xf_section = XF_Section()

