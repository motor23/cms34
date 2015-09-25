# -*- coding: utf-8 -*-
from cms34.stream import (
    StreamFactory,
    SFP_Tree,
    TypedItemFormFactory,
    SFP_FileUpload,
    SFP_ImageUpload,
)
from cms34.mixed import (
    XF_String,
    XF_Block,
    xf_id,
    xf_slug,
    xf_order,
    xf_type,
    xf_parent,
    xb_object,
)
from .fields import (
    xf_section_tree_title,
    xb_section_object,
)


class SFY_Sections(StreamFactory):
    name = 'sections'
    model = 'Section'
    title = u'Разделы'
    sort_initial_field = 'order'
    plugins = [SFP_Tree, SFP_FileUpload, SFP_ImageUpload]
    item_form_factory = TypedItemFormFactory
    obj_endpoint = True

    permissions = {
        'wheel': 'rwxdcp',
        'editor': 'rwxdcp',
    }

    list_fields = [
        xf_id,
        xf_section_tree_title,
        XF_String('tree_path', label=u'url'),
        xf_order,
    ]
    filter_fields = [
        xf_section_tree_title,
        xf_type,
    ]
    item_fields = {}
    default_item_fields = [xb_section_object]

    resources = []

    def __init__(self, register, resources=None, name=None, **kwargs):
        # Create child factories
        # XXX It's must be after plugins?
        if resources is None:
            resources = []
        self.resources = resources
        item_fields = dict(self.item_fields)
        for r in self.resources:
            if not r.section_model_factory:
                continue
            fields = r.section_stream_item_fields or self.default_item_fields
            item_fields[r.name] = fields
        self.item_fields = item_fields
        StreamFactory.__init__(self, register, name=name, **kwargs)


