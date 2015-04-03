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


class MFY_Org(ModelFactory):
    title = u'Организация'
    model = 'Org'

    fields = [
        xf_id,
        xf_title,
        xf_body,
        xf_members,
    ]


class MFY_OrgsListSection(ModelFactory):
    title = u'Список организаций'
    model = 'OrgsListSection'

    fields = [xf_id]
