# -*- coding: utf8 -*-
from .. import ResourceBase
from .models import (
    MFY_Media,
    MFY_Photo,
    MFY_Video,
    MFY_File,
    MFY_PhotoSet,
    MFY_MediaListSection,
)
from .streams import SFY_Multimedia, SFY_MediaListSection
from .front import V_MediaListSection

class R_Multimedia(ResourceBase):
    name = 'multimedia'
    title = u'Мультимедиa'

    model_factories = [MFY_Media]
    stream_factories = [SFY_Multimedia]


class R_MediaListSection(ResourceBase):
    name = 'media_list'
    title = u'Список медиа'

    view_cls = V_MediaListSection
    section_model_factory = MFY_MediaListSection
    section_stream_item_fields = SFY_MediaListSection.item_fields
    stream_factories = [SFY_MediaListSection]
