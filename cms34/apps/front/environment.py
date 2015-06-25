# -*- coding: utf-8 -*-
from iktomi.utils.storage import (storage_cached_property,
                                  storage_method,
                                  storage_property)
from iktomi.utils import cached_property
from jinja2 import Markup

from ..common.environment import Environment as EnvironmentBase
from ..common.replace_tags import replace_tags

import models


class Context(EnvironmentBase.Context):

    def css_tag(self, filename, media='screen, projection'):
        url = self.env.url_for_static('css/{}'.format(filename))
        return Markup('<link rel="stylesheet" type="text/css" '\
                      'media="{}" href="{}"/>'.format(media, url))

    def js_tag(self, filename):
        url = self.env.url_for_static('js/{}'.format(filename))
        return Markup('<script type="text/javascript" src="{}">'\
                      '</script>'.format(url))

    def preview_buttons(self, item, buttons=['edit']):
        if not getattr(self.env.cfg, 'PREVIEW', False):
            return u''
        parent_env = self.env.parent_env
        parent_env._push(models=self.env.models, lang=self.env.lang)
        result = parent_env.context.preview_buttons(item, buttons)
        parent_env._pop()
        return result



class Environment(EnvironmentBase):
    Context = Context
    shared_models = models.shared
    models = models.front

    def get_template_globals(self, env):
        result = EnvironmentBase.get_template_globals(self, env)
        return dict(result,
            replace_tags=replace_tags,
            lang=env.lang,
        )

    def url_for_obj(self, obj):
        raise NotImplementedError

    @cached_property
    def cached_db(self):
        return self.app.cached_db_maker()
