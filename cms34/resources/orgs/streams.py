# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
)
from cms34.mixed import (
    XF_Block,
    XB_Content,
    xf_body,
)
from .fields import xf_members
from ..sections.fields import (
    xb_section_object
)


class XB_Content(XB_Content):
    item_fields = [xf_body]


class XB_Members(XF_Block):
    name = 'org_persons_block'
    label = u'Члены'
    item_fields = [
        xf_members,
    ]

xb_content = XB_Content()
xb_members = XB_Members()


class SFY_Orgs(StreamFactory):
    name = 'orgs'
    model = 'Org'
    title = u'Организации'
    limit = 40
    preview = True
    sort_initial_field = 'title'

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    fields = [
        xb_section_object,
        xb_content,
        xb_members,
    ]
    list_fields = sort_fields = filter_fields = item_fields = fields


