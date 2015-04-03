# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_EventsList
from .models import MFY_EventsListSection


class R_EventsList(ResourceBase):
    name = 'events_list'
    title = u'Список событий'

    view_cls = front.V_EventsList
    section_model = models.MFY_EventsListSection

