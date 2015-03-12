# -*- coding: utf8 -*-
from iktomi.cms.stream import ListField, ItemLockListField

__all__ = (
    'LF_Base',
    'LF_String',
    'LF_Id',
    'LF_Relation',
    'LF_Img',
    'LF_Preview',
    'LF_PreviewRelation',
    'LF_DateTime',
    'lf_id',
    'lf_preview',
    'lf_preview_relation',
)

class LF_Base(object):
    name = None
    label = None
    width = 'auto'
    link_to_item = True
    template = ListField.template

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def list_field(self, fields_dict):
        fields_dict[self.name] = ListField(self.name, self.label, self.width,
                                           transform=self.transform,
                                           link_to_item=self.link_to_item,
                                           template=self.template)

    def transform(self, value):
        if value is None:
            return u'-'
        else:
            return value


class LF_String(LF_Base): pass


class LF_Id(LF_String):
    name = 'id'
    label = 'ID'
    width = '0%'

    def list_field(self, fields_dict):
        LF_String.list_field(self, fields_dict)
        fields_dict['%s_locked' % self.name] = ItemLockListField()


class LF_Relation(LF_String):
    multiple = False
    rel_prop_name = 'title'

    def transform(self, value):
        if not value:
            return u'-'
        if self.multiple:
            return ' ,'.join(map(self.get_rel_value, value))
        else:
            return self.get_rel_value(value)

    def get_rel_value(self, item):
        return getattr(item, self.rel_prop_name)


class LF_Img(LF_Base):

    width='200px'

    def list_field(self, fields_dict):
        fields_dict[self.name] = ListField(self.name, self.label, self.width,
                                           image=True)

class LF_Preview(LF_Img):
    name = 'img_admin_preview'


class LF_PreviewRelation(LF_Img):

    name = 'photo'
    rel_prop_name = 'img_admin_preview'

    def transform(self, value):
        if not value:
            return u'-'
        return self.get_rel_value(value)

    def get_rel_value(self, item):
        return getattr(item, self.rel_prop_name)


class LF_DateTime(LF_Base):

    format='%d-%m-%Y %H:%M'

    def transform(self, value):
        if value:
            return value.strftime(self.format)
        return u'-'


lf_id = LF_Id()
lf_preview = LF_Preview()
lf_preview_relation = LF_PreviewRelation()

