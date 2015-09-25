# -*- coding: utf-8 -*-

from cms34.resources import ResourceBase
from .models import MFY_Form, MFY_FormField
from .streams import SFY_FormFields


class R_FormConstructor(ResourceBase):
    name = 'form_constructor'
    title = u'Конструктор форм'

    model_factories = [MFY_Form]


class R_FormField(ResourceBase):
    name = 'form_field'
    title = u'Поле для конструктора форм'

    model_factories = [MFY_FormField]
    stream_factories = [SFY_FormFields]
