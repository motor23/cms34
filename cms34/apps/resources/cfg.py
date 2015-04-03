# -*- coding: utf-8 -*-
from os import path
import sys
import memcache
from collections import OrderedDict

from ..front.cfg import Cfg as CfgBase
import iktomi.templates, iktomi.cms


class Cfg(CfgBase):

    CMS34_DIR = path.dirname(path.abspath(__file__))

