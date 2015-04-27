# -*- coding: utf8 -*-
from ...model.factories import ModelFactory, MFP_Types
from ...mixed.fields import (
    xf_id,
    xf_title,
    xf_slug,
    xf_order,
    xf_parent,
)


class MFY_Section(ModelFactory):
    title = u'Раздел'
    model = 'Section'
    plugins = [MFP_Types]

    fields = [
        xf_id,
        xf_slug,
        xf_parent,
        xf_title,
        xf_order,
    ]
    types = []
    resources = []

    def __init__(self, register, resources=[], **kwargs):
        self.resources = resources
        r_types = [(r.name, r.section_model_factory) for r in self.resources \
                                                   if r.section_model_factory]
        self.types = self.types + r_types
        ModelFactory.__init__(self, register, **kwargs)


class MFY_DirSection(ModelFactory):
    title = u'Папка'
    model = 'DirSection'

    fields = [xf_id]

