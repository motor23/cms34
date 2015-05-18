# -*- coding: utf8 -*-
from iktomi.forms import convs

from cms34.mixed.fields import (
    XF_Id,
    XF_StreamSelect,
    XF_Block,
)
from cms34.stream.item_fields import (
    IF_StreamSelect,
)
from ....stream.item_fields import (
    IF_StreamSelect,
)
from .model import (
    MF_RegionId,
    MF_Region,
    MF_Regions,
)

__all__ = (
    'XF_Tags'
    'XF_RegionId',
    'XF_Region',
    'XF_Regions',
    'XB_Tags',
    'XB_Regions',
    'xf_region_id',
    'xf_tags',
    'xf_region',
    'xf_regions',
    'xb_tags',
    'xb_regions',
)

class XF_Tags(XF_StreamSelect):
    name = 'tags'
    label = u'Теги'
    model = 'Tag'
    stream_name = 'tags'
    ordered = True
    multiple = True


class XF_RegionId(XF_Id):

    def _model_field(self, factory=None):
        return MF_RegionId(self.name)


class XF_RegionSelect(XF_StreamSelect):

    model = 'Region'
    stream_name = 'regions'

    def _model_field(self, factory=None):
        if self.multiple:
            return MF_Regions(
                self.name,
                ordered=self.ordered,
                remote_cls_name=self.model,
            )
        else:
            return MF_Region(
                self.name,
                remote_cls_name=self.model,
            )

    def _item_field(self, models, factory=None):
        return IF_StreamSelect(
            self.name,
            label=self.label,
            model=self.model,
            stream_name=self.stream_name,
            multiple=self.multiple,
            allow_create=self.allow_create,
            allow_select=self.allow_select,
            allow_delete=self.allow_delete,
            inshift=self.inshift,
            condition=self.condition,
            default_filters=self.default_filters,
            ordered=self.ordered,
            rel=self.rel,
            conv=convs.Char()
        )



class XF_Region(XF_RegionSelect):
    name = 'region'
    label = u'Регион'
    multiple = False


class XF_Regions(XF_RegionSelect):
    name = 'regions'
    label = u'Регионы'
    multiple = True


xf_region_id = XF_RegionId()
xf_tags = XF_Tags()
xf_region = XF_Region()
xf_regions = XF_Regions()


class XB_Tags(XF_Block):
    name = 'region_block'
    label = u'Классификаторы'
    fields = [xf_tags]


class XB_Region(XF_Block):
    name = 'region_block'
    label = u'Регион'
    fields = [xf_region]

xb_tags = XB_Tags()
xb_region = XB_Region()

