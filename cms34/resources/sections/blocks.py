# -*- coding: utf-8 -*-
from cms34.mixed import (
    XB_Object,
    xf_id,
    xf_title,
    xf_type,
    xf_slug,
    xf_order,
    XF_Block,
)
from cms34.resources.sections.fields import (
    xf_section_parent,
    xf_section,
    xf_sections,
)


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
