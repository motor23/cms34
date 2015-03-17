# -*- coding: utf-8 -*-
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property

from ..common.environment import Environment as EnvironmentBase
import models


class Context(EnvironmentBase.Context): pass


class Environment(EnvironmentBase):
    Context = Context
    shared_models = models.shared
    models = models.front

