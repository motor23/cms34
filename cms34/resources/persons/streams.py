# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
    SFP_ImageUpload,
    SFP_SectionHtmlBodyHandler,
)
from cms34.mixed import (
    XF_Block,
    xb_object,
    XF_Img,
)
from .fields import (
    xf_first_name,
    xf_last_name,
    xf_patronymic,
    xf_post,
)
from cms34.resources.sections.blocks import xb_section_object


class XB_Main(XF_Block):
    name = 'person_block'
    label = u'Персона'

    fields = [
        xf_last_name,
        xf_first_name,
        xf_patronymic,
        xf_post,
    ]

    list_fields = sort_fields = filter_fields = item_fields = fields


class XB_Photo(XF_Block):
    name = 'photo_block'
    label = u'Фото'
    item_fields = [
        XF_Img(name='img_orig',
               label=u'Фото в исходном разрешении (Не более 5000×5000)',
               required=True),
    ]


xb_main = XB_Main()
xb_photo = XB_Photo()


class SFY_Persons(StreamFactory):
    name = 'persons'
    model = 'Person'
    title = u'Персоны'
    limit = 40
    preview = True
    sort_initial_field = 'title'

    permissions = {
        'wheel': 'rwxdcp',
        'editor': 'rwxdcp',
    }
    plugins = [
        SFP_ImageUpload,
        SFP_SectionHtmlBodyHandler,
    ]

    fields = [
        xb_section_object,
        xb_main,
        xb_photo,
    ]
    list_fields = sort_fields = filter_fields = item_fields = fields
