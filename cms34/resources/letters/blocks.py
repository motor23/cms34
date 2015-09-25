# -*- coding: utf-8 -*-
from cms34.mixed import XF_Block
from .fields import xf_rules


class XB_LettersSettings(XF_Block):
    name = 'letters_settings'
    label = u'Настройки обращений'
    fields = [
        xf_rules,
    ]


xb_letters_settings = XB_LettersSettings()
