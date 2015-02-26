# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
    SF_TreePlugin,
)
from ...mixed import (
    XF_String,
    XF_Block,
    xf_id,
    xf_slug,
    xf_tree_title,
    xf_order,
    xf_type,
    xf_parent,
    xb_object,
)


class XB_Main(XF_Block):
    name = 'main_block'
    label = u'Раздел'
    model_fields = ( #XXX
    )
    list_fields = (
        xf_id,
        xf_tree_title,
        XF_String('tree_path', label=u'url'),
        xf_type,
        xf_order,
    )
    sort_fields = (
        xf_id,
        xf_tree_title,
        xf_slug,
        xf_order,
    )
    filter_fields = (
        xf_id,
        xf_tree_title,
        xf_slug,
        xf_type,
    )
    item_fields = (
        xf_type,
        xf_parent,
        xf_slug,
        xf_order,
        xf_tree_title,
    )

xb_main = XB_Main()


class SectionsStreamFactory(StreamFactory):
    name = 'sections'
    model = 'Section'
    title = u'Разделы'
    initial_sort = 'order'
    plugins = [SF_TreePlugin]

    item_fields = (
        xb_object,
        xb_main,
    )
    list_fields = (
        xb_main,
    )
    sort_fields = (
        #section_block,
    )
    filter_fields = (
        xb_main,
    )

