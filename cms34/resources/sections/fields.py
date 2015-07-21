# -*- coding: utf8 -*-

from cms34.mixed import (
    XF_StreamSelect,
    XF_TreeTitle,
    XF_TypeImg,
    XF_Parent,
    XF_Block,
    XB_Object,
    xf_id,
    xf_title,
    xf_slug,
    xf_type,
    xf_order,
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


class XB_SectionObject(XB_Object):
    list_fields = [
        xf_id,
        xf_title,
    ]
    filter_fields = sort_fields = list_fields
    item_fields = [
        xf_id,
        xf_type,
        xf_section_parent,
        xf_slug,
        xf_order,
        xf_title,
    ]


xf_section = XF_Section()
xf_sections = XF_Sections()
xf_section_tree_title  = XF_SectionTreeTitle()
xb_section_object = XB_SectionObject()


class XB_Section(XF_Block):
    label = u'Раздел'
    name = 'section_block'
    fields = [
        xf_section,
    ]

class XB_Sections(XF_Block):
    label = u'Разделы'
    name = 'sections_block'
    fields = [
        xf_sections,
    ]


xb_section = XB_Section()
xb_sections = XB_Sections()

