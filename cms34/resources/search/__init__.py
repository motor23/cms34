# -*- coding: utf-8 -*-

from cms34.resources import ResourceBase
from .front.views import V_Search
from .models import MFY_SearchSection
from .streams import SFY_SearchSection


class R_Search(ResourceBase):
    name = 'search'
    title = u'Поиск'

    view_cls = V_Search
    section_model_factory = MFY_SearchSection
    section_stream_item_fields = SFY_SearchSection.item_fields
    stream_factories = [SFY_SearchSection]
