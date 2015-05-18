# -*- coding: utf8 -*-
from ...model import ModelFactory
from ...mixed import (
    xf_id,
    xf_title,
    xf_lead,
    xf_dt,
    xf_publish_dt,
)

class Selection(ModelFactory):
    title = u'Выборка'

    fields = [
        xf_id,
        xf_title,
        xf_lead,
        xf_dt,
        xf_publish_dt,
    ]


class SelectionsListSection(ModelFactory):
    title = u'Список выборок'

