# -*- coding: utf-8 -*-

from cms34.mixed import (
    xf_id,
    xf_title,
    xf_type,
    xf_order,
)
from cms34.resources.sections.blocks import XB_SectionObject
from cms34.resources.sections.fields import (
    xf_section_parent,
)
from .fields import (
    xf_search_slug,
)


class XB_SearchSectionObject(XB_SectionObject):
    item_fields = [
        xf_id,
        xf_type,
        xf_section_parent,
        xf_search_slug,
        xf_order,
        xf_title,
    ]


xb_search_section_object = XB_SearchSectionObject()