# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import MFY_Person
from .streams import SFY_Persons
from .front import V_Person, V_PersonsList


class R_Person(ResourceBase):
    name = 'person'
    title = u'Персона'

    view_cls = front.V_Person
    section_model_factory = MFY_Person
    section_stream_item_fields = SFY_Persons.fields
    stream_factories = [SFY_Persons]


class R_PersonsList(ResourceBase):
    name = 'persons_list'
    title = u'Список персон'

    view_cls = front.V_PersonsList
    section_model_factory = models.PersonsListSection
