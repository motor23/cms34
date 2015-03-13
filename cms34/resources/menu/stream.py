# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
    SFP_Tree,
)
from ...mixed import (
    XF_Block,
    xf_tree_title,
    xf_slug,
    xf_parent,
    xf_order,
    xb_object,
)


class XB_Main(XF_Block):
    name = 'menu_block'
    label = u'Меню'
    list_fields = [
        xf_tree_title,
        xf_order,
        #StdText(name='tree_path', label=u'url'),
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
    ]


xb_main = XB_Main()


class MenuStreamFactory(StreamFactory):
    stream_name = 'menu'
    model = 'Menu'
    title = u'Меню'
    initial_sort = 'order'
    plugins = [SFP_Tree]

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

