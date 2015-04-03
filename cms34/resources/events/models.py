# -*- coding: utf8 -*-
from cms34.model import (
    ModelFactory,
)
from cms34.mixed import (
    xf_id,
    xf_dt,
    xf_publish_dt,
    xf_title,
    xf_lead,
    xf_body,
)


class MFY_Event(ModelFactory):
    title = u'Событие'
    model = 'Event'

    fields = [
        xf_id,
        xf_dt,
        xf_publish_dt,
        xf_title,
        xf_lead,
        xf_body,
    ]


class MFY_EventsListSection(ModelFactory):
    title = u'Список событий'
    model = 'EventsListSection'

    fields = [xf_id]

