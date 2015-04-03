# -*- coding: utf8 -*-
from .. import ResourceBase
from . import front, models


class R_Page(ResourceBase):
    name = 'page'
    title = u'Страницы'

    view_cls = front.V_Page
    section_model = models.Page
