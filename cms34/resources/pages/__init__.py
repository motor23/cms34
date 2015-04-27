# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_Page
from .models import MFY_Page
from .streams import SFY_Pages


class R_Page(ResourceBase):
    name = 'page'
    title = u'Страницы'

    view_cls = V_Page
    section_model_factory = MFY_Page
    section_stream_item_fields = SFY_Pages.fields
    stream_factories = [SFY_Pages]
