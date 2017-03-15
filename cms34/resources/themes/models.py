# -*- coding: utf8 -*-
from ...model import ModelFactory
from ...mixed import (
    xf_id,
    xf_title,
    xf_lead,
    xf_dt,
    xf_publish_dt,
    xf_body,
)

class MFY_Theme(ModelFactory):
    title = u'Тема'
    model = 'Theme'

    fields = [
        xf_id,
        xf_lead,
        xf_body,
    ]


class MFY_ThemesListSection(ModelFactory):
    title = u'Список тем'
    model = 'ThemesListSection'

    fields = [
        xf_id,
    ]
