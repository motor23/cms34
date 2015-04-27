# -*- coding: utf8 -*-
from cms34.model import ModelFactory
from cms34.mixed import (
    xf_id,
    xf_parent,
    xf_title,
    xf_order,
)
from ..sections.fields import xf_section


class MFY_Menu(ModelFactory):
    model = 'Menu'
    title = u'Меню'

    fields = [
        xf_id,
        xf_parent,
        xf_title,
        xf_order,
        xf_section,
    ]

