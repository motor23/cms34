# -*- coding: utf8 -*-
from ...model import (
    ModelFactory,
)

from ...mixed import (
    xf_id,
    xf_title,
    xf_body,
)

from .fields import xf_members


class Org(ModelFactory):
    title = u'Организация'

    fields = (
        xf_id,
        xf_title,
        xf_body,
        xf_members,
    )

class OrgsListSection(ModelFactory):
    title = u'Список организаций'
