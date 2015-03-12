# -*- coding: utf8 -*-
from ...model.factories import ModelFactory, SingleTableTypesPlugin
from ...mixed.fields import (
    xf_id,
    xf_title,
    xf_slug,
    xf_order,
    xf_parent,
)

class EmptySection(ModelFactory):
    title = u'Папка'

class Section(ModelFactory):
    title = u'Раздел'
    plugins = [SingleTableTypesPlugin]

    fields = [
        xf_id,
        xf_slug,
        xf_parent,
        xf_title,
        xf_order,
    ]
    types = [('404', EmptySection),]

