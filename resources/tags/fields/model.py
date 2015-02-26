from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relation

from ....model.fields import (
    MF_String,
    MF_Id,
    MF_M2MRelation,
    MF_M2ORelation,
)

class MF_RegionId(MF_Id):

    autoincrement = False

    class field_cls(MF_String):
        length=3


class MF_Region(MF_M2ORelation):
    name = 'region'
    remote_cls_name = 'Region'
    def get_dict(self, models, factory=None):
        remote_cls_name = self.get_remote_cls_name(factory)
        remote_cls = getattr(models, remote_cls_name)
        field_id = Column(String(3),
                          ForeignKey(remote_cls.id, ondelete=self.ondelete),
                          primary_key=self.primary_key,
                          nullable=self.nullable)
        field = relation(remote_cls, remote_side=remote_cls.id)

        @property
        def field_title(_self):
            obj = getattr(_self, self.name)
            if obj:
                return obj.title

        return {
            '%s_id' % self.name: field_id,
            '%s_title' % self.name: field_title,
            self.name: field,
        }


class MF_Regions(MF_M2MRelation):
    name = 'regions'
    remote_cls_name = 'Region'

    def get_rel_cls_fields(self, factory=None):
        cls_name = self.get_cls_name(factory)
        remote_cls_name = self.get_remote_cls_name()
        return [
            MF_M2ORelation(
                cls_name.lower(),
                remote_cls_name = cls_name,
                nullable = False,
                ondelete = 'cascade',
                primary_key = True,
            ),
            MF_Region(
                remote_cls_name.lower(),
                remote_cls_name = remote_cls_name,
                nullable = False,
                ondelete = 'cascade',
                primary_key = True,
            ),
        ]

