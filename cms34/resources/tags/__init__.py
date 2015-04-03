# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_RegionSection
from .models import MFY_RegionSection


class R_RegionSection(ResourceBase):
    name = 'region'
    title = u'Регион'

    view_cls = front.V_RegionSection
    section_model = models.MFY_RegionSection

