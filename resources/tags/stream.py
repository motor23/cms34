# -*- coding:utf8 -*-
from ...stream import (
    StreamFactory,
)
from ...mixed import (
    xf_title,
)
from .fields import (
    xf_region_id,
)

class RegionsStreamFactory(StreamFactory):
    name = 'regions'
    model = 'Region'
    title = u'Регионы'
    limit = 40
    initial_sort = 'title'
    permissions = {'wheel': 'x'}

    fields = [xf_region_id, xf_title]
    item_fields = list_fields = sort_fields = fields
    filter_fields = [xf_region_id, xf_title]
