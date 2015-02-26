# -*- coding: utf8 -*-
from ...model.factories import ModelFactory
from ...mixed import (
    xf_id,
    xf_title,
)
from .fields import xf_region_id

class Tag(ModelFactory):
    title = u'Тег'

    fields = [
        xf_id,
        xf_title,
    ]


class Region(ModelFactory):
    title = u'Регионы'

    fields = [
        xf_region_id,
        xf_title,
    ]

