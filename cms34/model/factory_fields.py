from .fields import (
    MF_O2MRelation,
    MF_M2ORelation,
    mf_id,
    mf_order,
)
from .factories import ModelFactory
from ..utils import prop_getter

__all__ = (
    'MF_List',
)

class MF_List(MF_O2MRelation):

    ordered = True
    remote_factory_cls = ModelFactory
    remote_factory_bases = None
    get_remote_factory_bases = prop_getter('remote_factory_bases',
                                           'rel_cls_bases')
    remote_factory_plugins = []
    fields = []
    remote_foreign_key=True

    def register(self, factory, register):
        cls_name = self.get_cls_name(factory)
        fields = [
                mf_id,
                MF_M2ORelation(cls_name.lower(), remote_cls_name=cls_name),
        ] + self.fields
        if self.ordered:
            fields.append(mf_order)
        remote_cls_name = self.get_remote_cls_name(factory)
        remote_factory_bases = self.get_remote_factory_bases(factory)
        type(remote_cls_name, (self.remote_factory_cls,), dict(
                bases=remote_factory_bases,
                rel_cls_bases=remote_factory_bases,
                plugins=self.remote_factory_plugins,
                fields=fields,
        ))(register, main_factory=factory)

