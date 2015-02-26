# -*- coding: utf8 -*-

from ....mixed.fields import (
    XF_Id,
    XF_StreamSelect,
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
    'xf_region_id',
    'xf_tags',
    'xf_region',
    'xf_regions',
)

class XF_Tags(XF_StreamSelect):
    name = 'tags'
    remote_cls_name = 'Tag'
    ordered = False


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

