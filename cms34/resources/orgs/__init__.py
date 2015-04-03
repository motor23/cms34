# -*- coding: utf8 -*-
from .. import ResourceBase
from .front import V_Org, V_OrgsList
from .models import MFY_Org, MFY_OrgsListSection


class R_Org(ResourceBase):
    name = 'org'
    title = u'Организация'

    view_cls = front.V_Org
    section_model = models.MFY_Org


class R_OrgsList(ResourceBase):
    name = 'orgs_list'
    title = u'Список организаций'

    view_cls = front.V_OrgsList
    section_model = models.MFY_OrgsListSection

