# -*- coding: utf-8 -*-
from webob.exc import HTTPNotFound
from iktomi.web import match, cases

from common.handlers.context import BaseContext, HContext
from common.models.std import Factory

name = 'persons_list'
title = u'Список персон'

class Section(Factory):
    title = title


