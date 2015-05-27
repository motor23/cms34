# -*- coding: utf8 -*-
from collections import OrderedDict

from iktomi.cms.stream import ListField, ItemLockListField

__all__ = (
    'LF_Base',
    'LF_String',
    'LF_Title',
    'LF_Id',
    'LF_Relation',
    'LF_Img',
    'LF_AdminPreview',
    'LF_PreviewRelation',
    'LF_DateTime',
    'LF_TreeTitle',
    'LF_TreeExpand',
    'LF_Container',
    'LF_TreeExpand',
    'LF_TreeTitle',
    'LF_SimpleImg',
    'LF_EnumImg',
    'lf_title',
    'lf_id',
    'lf_admin_preview',
    'lf_preview_relation',
    'lf_tree_title',
    'lf_tree_expand',
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
        raise NotImplementedError()


class LF_String(LF_Base):

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


class LF_Title(LF_String):
    name = 'title'
    label = u'Заголовок'


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


class LF_AdminPreview(LF_Img):
    name = 'img_admin_preview'
    label = u'Превью'


class LF_PreviewRelation(LF_Img):

    name = 'photo'
    rel_prop_name = 'img_admin_preview'

    def transform(self, value):
        if not value:
            return u'-'
        return self.get_rel_value(value)

    def get_rel_value(self, item):
        return getattr(item, self.rel_prop_name)


class LF_DateTime(LF_String):

    format='%d-%m-%Y %H:%M'

    def transform(self, value):
        if value:
            return value.strftime(self.format)
        return u'-'


class SimpleListField(ListField):
    width = 'auto'
    link_to_item = True
    width = ''
    transform = None

    def __init__(self, name, title, template, **kwargs):
        self.name = name
        self.title = title
        self.template = template
        self.__dict__.update(kwargs)

    def get_value(self, env, item, url, loop):
        return


class LF_Container(LF_Base):
    template = 'list_fields/container.html'
    fields = []

    def list_field(self, fields_dict):
        _fields_dict = OrderedDict()
        for field in self.fields:
            field.list_field(_fields_dict)
        fields_dict[self.name] = SimpleListField(
                                           self.name, self.label,
                                           width=self.width,
                                           fields=_fields_dict.values(),
                                           link_to_item=False,
                                           template=self.template,
        )


class LF_TreeExpand(LF_Base):
    name = 'tree_expand'
    template = 'list_fields/tree_expand.html'
    width="25px"

    def list_field(self, fields_dict):
        fields_dict[self.name] = SimpleListField(
                                           self.name, self.label,
                                           link_to_item=False,
                                           width=self.width,
                                           template=self.template)

class LF_SimpleImg(LF_Base):
    template = 'list_fields/simple_img.html'
    width="25px"

    def list_field(self, fields_dict):
        fields_dict[self.name] = SimpleListField(
                                           self.name, self.label,
                                           link_to_item=self.link_to_item,
                                           width=self.width,
                                           get_value=self.get_value,
                                           template=self.template)

    def get_value(self, env, item, url, loop):
        raise NotImplementedError()


class LF_EnumImg(LF_SimpleImg):

    img_url_template = '/cms34-static/img/%(name)s/%(value)s.png'

    def get_value(self, env, item, url, loop):
        value = getattr(item, self.name)
        title = getattr(item, '%s_name' % self.name)
        url = self.img_url_template % {'name': self.name, 'value':value}
        return dict(
            url=url,
            title=title,
        )


lf_id = LF_Id()
lf_title = LF_Title()
lf_admin_preview = LF_AdminPreview()
lf_preview_relation = LF_PreviewRelation()
lf_tree_expand = LF_TreeExpand()


class LF_TreeTitle(LF_Container):
    name = 'tree_title'
    fields = [lf_tree_expand, lf_title]


lf_tree_title = LF_TreeTitle()
