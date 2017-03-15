# -*- coding: utf8 -*-

from cms34.mixed import (
    XF_StreamSelect,
    XF_TreeTitle,
    XF_TypeImg,
    XF_Parent,
)
from cms34.stream import (
    lf_tree_expand,
    LF_String,
)


class XF_Section(XF_StreamSelect):
    name = 'section'
    label = u'Раздел'
    model = 'Section'
    stream_name = 'sections'


class XF_SectionRequired(XF_Section):
    required = True


class XF_Sections(XF_Section):
    name = 'sections'
    label = u'Разделы'
    model = 'Section'
    stream_name = 'sections'
    multiple = True


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


class XF_SectionParent(XF_Parent):
    stream_name = 'sections'
    model = 'Section'


xf_section_parent = XF_SectionParent()

xf_section = XF_Section()
xf_section_required = XF_SectionRequired()
xf_sections = XF_Sections()
xf_section_tree_title = XF_SectionTreeTitle()


