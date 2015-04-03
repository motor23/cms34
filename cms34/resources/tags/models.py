# -*- coding: utf8 -*-
from ...model.factories import ModelFactory
from ...mixed import (
    xf_id,
    xf_title,
)
from .fields import xf_region_id, xf_region

class MFY_Tag(ModelFactory):
    title = u'Тег'
    model = 'Tag'

    fields = [
        xf_id,
        xf_title,
    ]


class MFY_Region(ModelFactory):
    title = u'Регионы'
    model = 'Region'

    fields = [
        xf_region_id,
        xf_title,
    ]


class MFY_RegionSection(ModelFactory):
    title = u'Регион'
    model = 'RegionSection'

    fields = [
        xf_id,
        xf_region,
    ]

