# -*- coding: utf-8 -*-
from common.fields import MF_Json
from cms34.model.fields import MF_Int
from cms34.model.fields import MF_DateTime
from cms34.mixed.fields import (
    XF_Body,
)


class MF_LetterJson(MF_Json):
    name = 'letter_json'


class XF_Rules(XF_Body):
    name = 'rules'
    label = u'Правила отправки обращений'


class MF_SendDateTime(MF_DateTime):
    name = 'send_dt'
    default = None
    required = False


class MF_SectionId(MF_Int):
    # We cannot store relation between databases, so keep only id
    name = 'section_id'
    required = True


xf_rules = XF_Rules()
mf_letter_json = MF_LetterJson()
mf_send_dt = MF_SendDateTime()
mf_section_id = MF_SectionId()
