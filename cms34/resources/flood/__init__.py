# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import MFY_FloodProtection


class R_FloodProtection(ResourceBase):
    name = 'FloodProtection'
    title = u'Защита от флуда'

    model_factories = [MFY_FloodProtection]
