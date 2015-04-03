# -*- coding: utf8 -*-
from ...model.factories import ModelFactory, SingleTableTypesPlugin
from ...mixed.fields import (
    xf_id,
    xf_title,
    xf_slug,
    xf_order,
    xf_parent,
)


class MFY_Section(ModelFactory):
    title = u'Раздел'
    name = 'Section'
    plugins = [SingleTableTypesPlugin]

    fields = [
        xf_id,
        xf_slug,
        xf_parent,
        xf_title,
        xf_order,
    ]
    types = []
    resources = []

    def __init__(self, *args, **kwargs):
        self.types += [(r.name, r.section_model) for r in self.resources]
        ModelFactory.__init__(self, *args, **kwargs)


class MFY_DirSection(ModelFactory):
    title = u'Папка'
    model = 'DirSection'

    fields = [xf_id]

