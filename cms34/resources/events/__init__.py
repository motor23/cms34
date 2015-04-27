# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_EventsList
from .models import MFY_Event, MFY_EventsListSection
from .streams import SFY_Events


class R_EventsList(ResourceBase):
    name = 'events_list'
    title = u'Список событий'

    view_cls = V_EventsList
    section_model_factory = MFY_EventsListSection
    model_factories = [MFY_Event]
    stream_factories = [SFY_Events]

