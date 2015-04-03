# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_Theme, V_ThemesList
from .models import MFY_Theme, MFY_ThemesListSection


class R_Theme(ResourceBase):
    name = 'theme'
    title = u'Тема'

    view_cls = front.V_Theme
    section_model = models.MFY_Theme


class R_ThemesList(ResourceBase):
    name = 'themes_list'
    title = u'Список тем'

    view_cls = front.V_ThemesList
    section_model = models.MFY_ThemesListSection

