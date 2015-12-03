# -*- coding: utf-8 -*-
import json
from sqlalchemy import PickleType, Text, Column
from cms34.model.fields import MF_Int, MF_Base, MF_DateTime
from cms34.mixed.fields import XF_Body, XF_Simple


class TextPickleType(PickleType):
    impl = Text


class MF_Json(MF_Base):
    default = {}

    def get_dict(self, models, factory=None):
        field = Column(TextPickleType(pickler=json))
        return {self.name: field}


class XF_Json(XF_Simple):
    initial = {}

    def _model_field(self, factory=None):
        return MF_Json(self.name, default=self.initial)


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
