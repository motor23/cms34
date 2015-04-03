# -*- coding: utf8 -*-

from ...mixed import (
    XF_StreamSelect,
    XF_TreeTitle,
    XF_TypeImg,
)
from ...stream import (
    lf_tree_expand,
    LF_String,
)

class XF_Section(XF_StreamSelect):
    name = 'section'
    label = u'Раздел'
    model = 'Section'
    stream_name = 'sections'


class XF_SectionTreeTitle(XF_TreeTitle):
    img_url_template = '/cms34-static/img/sections/%(value)s.png'
    def container_list_fields(self):
        return [
            lf_tree_expand,
            XF_TypeImg(img_url_template=self.img_url_template),
            LF_String(self.name,
                label=self.label,
            ),
        ]

xf_section = XF_Section()
xf_section_tree_title  = XF_SectionTreeTitle()
