# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import MFY_Options
from .streams import SFY_Options

class R_Options(ResourceBase):
    name = 'options'
    title = u'Опции'

    model_factories = [MFY_Options]
    stream_factories = [SFY_Options]

