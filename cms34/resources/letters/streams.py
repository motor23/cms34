# -*- coding: utf-8 -*-
from cms34.stream import StreamFactory
from cms34.resources.sections.fields import xb_section_object
from cms34.resources.forms.fields import xb_form_blocks
from .blocks import xb_letters_settings


class SFY_LettersSection(StreamFactory):
    name = 'letters'
    model = 'LettersSection'
    title = u'Обращения'
    limit = 40
    preview = True
    sort_initial_field = 'id'

    permissions = {
        'wheel': 'rwxdcp',
        'editor': 'rwxdcp',
    }

    base_fields = []

    item_fields = [
        xb_section_object,
        xb_letters_settings,
        xb_form_blocks,
    ]
    list_fields = filter_fields = sort_fields = item_fields


class SFY_FeedbackSection(SFY_LettersSection):
    name = 'feedback'
    title = u'Обратная связь'

    item_fields = [
        xb_section_object,
        xb_form_blocks,
    ]
    list_fields = filter_fields = sort_fields = item_fields
