# -*- coding: utf-8 -*-
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property

from ..common.environment import Environment as EnvironmentBase
from ..common.replace_tags import replace_tags

import models


class Context(EnvironmentBase.Context): pass


class Environment(EnvironmentBase):
    Context = Context
    shared_models = models.shared
    models = models.front

    def get_template_globals(self, env):
        result = EnvironmentBase.get_template_globals(self, env)
        return dict(result,
            replace_tags=replace_tags
        )

    def url_for_obj(self, obj):
        raise NotImplementedError
