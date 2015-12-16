# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
    SFP_Tree,
)
from cms34.mixed import (
    XF_Block,
    xf_tree_title,
    xf_parent,
    xf_order,
    xb_object,
)
from ..sections.fields import xf_section_required


class XB_Main(XF_Block):
    name = 'menu_block'
    label = u'Меню'
    list_fields = [
        xf_tree_title,
        xf_order,
    ]
    sort_fields = [
        xf_order,
    ]
    filter_fields = [
    ]
    item_fields = [
        xf_order,
        xf_parent,
        xf_tree_title,
        xf_section_required,
    ]


xb_main = XB_Main()


class SFY_Menu(StreamFactory):
    name = 'menu'
    model = 'Menu'
    title = u'Меню'
    plugins = [SFP_Tree]
    sort_initial_field='order'

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    item_fields = [
        xb_object,
        xb_main,
    ]
    list_fields = [
        xb_object,
        xb_main,
    ]
    sort_fields = []
    filter_fields = []

