# -*- coding: utf8 -*-
from .. import ResourceBase
from ..sections.fields import xb_section_object
from .front import V_RegionSection
from .models import MFY_Region, MFY_RegionSection
from .streams import SFY_Regions
from .fields import xb_region


class R_Regions(ResourceBase):
    name = 'regions'
    model_factories = [MFY_Region]
    stream_factories = [SFY_Regions]


class R_RegionSection(ResourceBase):
    name = 'region'
    title = u'Регион'

    view_cls = V_RegionSection
    section_model_factory = MFY_RegionSection
    section_stream_item_fields = [xb_section_object, xb_region]
