# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_DirSection
from .models import MFY_DirSection


class R_Dir(ResourceBase):
    name = 'dir'
    title = u'Папка'

    view_cls = front.V_DirSection
    section_model = models.MFY_DirSection
