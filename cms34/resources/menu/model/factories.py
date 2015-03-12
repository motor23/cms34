# -*- coding: utf8 -*-
from ....model.factories import ModelFactory
from ....model.fields import (
    mf_id,
    mf_slug,
    mf_parent,
    mf_title,
    mf_order,
)


class Menu(ModelFactory):
    title = u'Меню'

    fields = [
        mf_id,
        mf_parent,
        mf_title,
        mf_order,
#        mf_base_methods,
#        mf_tree_methods,
    ]

