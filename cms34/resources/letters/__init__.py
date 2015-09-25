# -*- coding: utf-8 -*-

from cms34.resources import ResourceBase
from .front.views import V_LettersSection
from .models import MFY_LettersSection, MFY_Letter
from .streams import SFY_LettersSection, SFY_FeedbackSection


class R_Letters(ResourceBase):
    name = 'letters'
    title = u'Обращения'

    view_cls = V_LettersSection
    section_model_factory = MFY_LettersSection
    section_stream_item_fields = SFY_LettersSection.item_fields
    stream_factories = [SFY_LettersSection]


class R_Letter(ResourceBase):
    name = 'letter'
    title = u'Обращение'

    model_factories = [MFY_Letter]
