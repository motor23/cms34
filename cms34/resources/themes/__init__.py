# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_Theme, V_ThemesList
from .models import MFY_Theme, MFY_ThemesListSection
from .streams import SFY_Themes


class R_Theme(ResourceBase):
    name = 'theme'
    title = u'Тема'

    view_cls = V_Theme
    section_model_factory = MFY_Theme
    section_stream_item_fields = SFY_Themes.fields
    stream_factories = [SFY_Themes]


class R_ThemesList(ResourceBase):
    name = 'themes_list'
    title = u'Список тем'

    view_cls = V_ThemesList
    section_model_factory = MFY_ThemesListSection

