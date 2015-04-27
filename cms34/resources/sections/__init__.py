# -*- coding: utf8 -*-
from .. import ResourceBase, ResourcesBase
from .front import V_DirSection
from .models import MFY_DirSection, MFY_Section
from .streams import SFY_Sections

class Resources(ResourcesBase):
    sections_model_factory = MFY_Section
    sections_stream_factory = SFY_Sections


class R_Dir(ResourceBase):
    name = 'dir'
    title = u'Папка'

    section_model_factory = MFY_DirSection
    view_cls = front.V_DirSection
