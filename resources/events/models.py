# -*- coding: utf8 -*-
from cms34.model import (
    ModelFactory,
    mf_id,
    mf_dt,
    mf_publish_dt,
    mf_title,
    mf_lead,
    mf_body,
)

class Event(ModelFactory):
    title = u'Событие'

    fields = [
        mf_id,
        mf_dt,
        mf_publish_dt,
        mf_title,
        mf_lead,
        mf_body,
    ]

class EventsListSection(ModelFactory):
    title = u'Событие'

