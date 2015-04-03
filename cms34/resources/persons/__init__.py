# -*- coding: utf8 -*-
from .. import ResourceBase
from . import front, models


class R_Person(ResourceBase):
    name = 'person'
    title = u'Персона'

    view_cls = front.V_Person
    section_model = models.Person


class R_PersonsList(ResourceBase):
    name = 'persons_list'
    title = u'Список персон'

    view_cls = front.V_PersonsList
    section_model = models.PersonsListSection

