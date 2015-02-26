# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases

from common.handlers.context import BaseContext, HContext
from std.model.factories import ModelFactory
from std.model.fields import MF_M2ORelation

name = 'org'
title = u'Состав cовета'

class OrgSection(ModelFactory):
    title = title
    table = None
    identity = name
    item_fields = [MF_M2ORelation('org', remote_cls_name='Org'),]


def url_for_index(root):
    return root.index

def h_index(env, data):
    org = env.db.query(env.models.Org)\
                .filter_by(section_id=env.section.section.id).first()
    if not org:
        raise HTTPNotFound()
    return env.resource.render_to_response('index', dict(org=org))


class Context(BaseContext):

     name = name


handler = HContext('resource', Context) | cases(
              match('/', name='index') | h_index,)

