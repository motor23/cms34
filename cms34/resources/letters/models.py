# -*- coding: utf8 -*-
from cms34.model import (
    ModelFactory,
    mf_id,
    mf_dt,
)
from cms34.resources.forms.fields import xb_form_blocks
from .fields import mf_letter_json, mf_send_dt, mf_section_id
from .blocks import xb_letters_settings


class MFY_LettersSection(ModelFactory):
    title = u'Обращения'
    model = 'LettersSection'

    fields = [
        mf_id,
        xb_letters_settings,
        xb_form_blocks,
    ]


class MFY_Letter(ModelFactory):
    title = u'Обращение'
    model = 'Letter'

    fields = [
        mf_id,
        mf_letter_json,
        mf_dt,
        mf_send_dt,
        mf_section_id,
    ]
