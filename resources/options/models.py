# -*- coding: utf8 -*-
from cms34.model.factories import ModelFactory, SingleTableTypesPlugin
from cms34.model.fields import (
    mf_id,
    mf_publish_dt,
    mf_title,
    mf_order,
)

class Options(ModelFactory):
    title = u'Опции'
    plugins = [SingleTableTypesPlugin]
    fields = [
        mf_id,
        mf_publish_dt,
        mf_title,
        mf_order,
    ]
    types = [] #must be redefined
