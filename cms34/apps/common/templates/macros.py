# -*- coding: utf-8 -*-
import logging
from iktomi.utils import weakproxy

logger = logging.getLogger(__name__)

class MacrosModuleWrapper(object):

    def __init__(self, module):
        self.__module = module

    def __getattr__(self, name):
        return getattr(self.__module, name)

    def __call__(self, *args, **kwargs):
        return self.__module.main(*args, **kwargs)


class MacrosLib(object):

    def __init__(self, template):
        self.__template = weakproxy(template)

    def __getattr__(self, name):
        try:
            jinja = self.__template.env
            tmpl = jinja.get_template('macros/%s.html' % name)
            module = tmpl.make_module(vars=self.__template.env.globals)
            result = MacrosModuleWrapper(module)
            setattr(self, name, result)
            return result
        except Exception as e:
            logger.exception(e)
            raise



