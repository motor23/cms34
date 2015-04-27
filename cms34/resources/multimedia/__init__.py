# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import MFY_Media
from .streams import SFY_Multimedia


class R_Multimedia(ResourceBase):
    name = 'multimedia'
    title = u'Мультимедиa'

    model_factories = [MFY_Media]
    stream_factories = [SFY_Multimedia]

