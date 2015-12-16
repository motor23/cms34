# -*- coding: utf-8 -*-
from cms34.mixed import (
    xf_optional_title,
    XF_List,
)
from ..persons.fields import xf_persons


class XF_Members(XF_List):
    name = 'persons_blocks'
    model = 'OrgPersonsBlock'
    label = u'Члены'

    fields = [
        xf_optional_title,
        xf_persons,
    ]


xf_members = XF_Members()
