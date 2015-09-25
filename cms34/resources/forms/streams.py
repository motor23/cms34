# -*- coding: utf-8 -*-

from cms34.stream.factories import StreamFactory, TypedItemFormFactory
from cms34.mixed import xb_object, xf_type
from .fields import (
    XF_Block,
    xf_field_type,
    xf_required,
    xf_field_name,
    xf_title,
    xf_field_size,
    xf_options_list,
)


class XB_FieldOptions(XF_Block):
    name = 'field_options'
    label = u'Настройки поля'

    item_fields = [
        xf_field_type,
        xf_required,
        xf_field_name,
        xf_title,
        xf_field_size,
        xf_options_list,
    ]


xb_field_options = XB_FieldOptions()


class SFY_FormFields(StreamFactory):
    name = 'form_fields'
    title = u'Поля для конструктора форм'
    model = 'FormField'

    common_fields = [xb_object]

    item_fields = common_fields + [xb_field_options]

    sort_fields = filter_fields = list_fields = common_fields + [xb_object,
                                                                 xf_title,
                                                                 xf_type]
