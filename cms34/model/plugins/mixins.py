# -*- coding: utf-8 -*-
from functools import partial
from cms34.model import ModelFactoryPlugin


class _MFP_AddMixin(ModelFactoryPlugin):
    """
    Plugin for adding mixins to factories. Never use this class directly,
    you should instantiate it with constructor-function `MFP_AddMixin`.
    """

    def __init__(self, factory=None, **kwargs):
        super(_MFP_AddMixin, self).__init__(factory, **kwargs)

        _mixin = kwargs.get('_mixin', None)
        assert _mixin is not None, "Mixin is not provided. Use constructor " \
                                   "function `MFP_AddMixin`."
        if factory and _mixin:
            self._add_mixin(_mixin)

    def _add_mixin(self, mixin):
        assert self.factory, 'Factory is not specified'
        bases = getattr(self.factory, 'bases', [])
        self.factory.bases = bases + [mixin]


def MFP_AddMixin(mixin):
    return partial(_MFP_AddMixin, _mixin=mixin)
