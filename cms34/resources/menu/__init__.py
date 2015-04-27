# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import MFY_Menu
from .streams import SFY_Menu


class R_Menu(ResourceBase):
    name = 'menu'
    title = u'Меню'

    model_factories = [MFY_Menu]
    stream_factories = [SFY_Menu]

