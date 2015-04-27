# -*- coding: utf8 -*-
from cms34.model.factories import ModelFactory, MFP_SingleTableTypes
from cms34.model.fields import (
    mf_id,
    mf_publish_dt,
    mf_title,
    mf_order,
)

class MFY_Options(ModelFactory):
    model = 'Options'
    title = u'Опции'
    plugins = [MFP_SingleTableTypes]
    fields = [
        mf_id,
        mf_publish_dt,
        mf_title,
        mf_order,
    ]
    types = [] #must be redefined
