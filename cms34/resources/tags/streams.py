# -*- coding:utf8 -*-
from ...stream import (
    StreamFactory,
)
from cms34.mixed import (
    xf_id,
    xf_title,
)
from .fields import (
    xf_region_id,
)

class SFY_Tags(StreamFactory):
    name = 'tags'
    model = 'Tag'
    title = u'Теги'
    limit = 40
    initial_sort = 'title'

    fields = [xf_id, xf_title]
    item_fields = list_fields = filter_fields = sort_fields = fields


class SFY_Regions(StreamFactory):
    name = 'regions'
    model = 'Region'
    title = u'Регионы'
    limit = 40
    initial_sort = 'title'

    permissions = {
        'wheel':'x',
        'editor':'x',
    }

    fields = [xf_region_id, xf_title]
    item_fields = list_fields = sort_fields = fields
    filter_fields = [xf_region_id, xf_title]

