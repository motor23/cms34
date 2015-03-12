# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
)
from ...mixed import (
    XF_Block,
    xb_object,
    xf_title,
    xf_body,
)
from .fields import xf_members


class XB_Main(XF_Block):
    name = 'org_block'
    label = u'Организация'
    list_fields = [
        xf_title,
    ]
    sort_fields = [
        xf_title,
    ]
    filter_fields = [
        xf_title,
    ]
    item_fields = [
        xf_title,
        xf_body,
    ]


class XB_Members(XF_Block):
    name = 'org_persons_block'
    label = u'Члены'
    item_fields = [
        xf_members,
    ]


xb_main = XB_Main()
xb_members = XB_Members()


class OrgsStreamFactory(StreamFactory):
    name = 'orgs'
    model = 'Org'
    title = u'Организации'
    limit = 40
    preview = True

    blocks = [
        xb_object,
        xb_main,
        xb_members,
    ]
    list_fields = sort_fields = filter_fields = item_fields = blocks


