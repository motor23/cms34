# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_Org, V_OrgsList
from .models import MFY_Org, MFY_OrgsListSection
from .streams import SFY_Orgs


class R_Org(ResourceBase):
    name = 'org'
    title = u'Организация'

    view_cls = V_Org
    section_model_factory = MFY_Org
    section_stream_item_fields = SFY_Orgs.fields
    stream_factories = [SFY_Orgs]


class R_OrgsList(ResourceBase):
    name = 'orgs_list'
    title = u'Список организаций'

    view_cls = V_OrgsList
    section_model_factory = MFY_OrgsListSection

