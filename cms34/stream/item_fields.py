# -*- coding: utf8 -*-
from collections import OrderedDict

from iktomi.utils import cached_property
from iktomi.forms import Field
from iktomi.cms.forms import convs, widgets, fields

from .convs import (
    NoUpperConv,
    StripTrailingDotConv,
)

__all__ = (
    'IF_Base',
    'IF_String',
    'IF_Text',
    'IF_Title',
    'IF_Int',
    'IF_Id',
    'IF_HiddenId',
    'IF_Bool',
    'IF_Select',
    'IF_StreamSelect',
    'IF_File',
    'IF_Img',
    'IF_Block',
    'IF_DateTime',
    'IF_List',
    'if_title',
    'if_id',
    'if_hidden_id',
)

PermissionsGetter=str #XXX

class IF_Base(object):
    label = None
    name = None
    permissions = "rw"
    permissions_getter = PermissionsGetter

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def item_field(self, fields_dict, models, factory=None):
        raise NotImplementedError()

    def item_form(self, fields_dict, models, factory=None): pass


class IF_Simple(IF_Base):
    required = False
    initial = None

    def item_field(self, fields_dict, models, factory=None):
        fields_dict[self.name] = self.create_field(models, factory)

    def create_field(self, models, factory=None):
        kwargs = {}
        if self.initial is not None:
            kwargs['initial'] = self.initial
        return Field(
            self.name,
            conv=self.create_conv(models, factory),
            widget=self.create_widget(models, factory),
            permissions=self.permissions_getter(self.permissions),
            label=self.label,
            **kwargs
        )

    def create_conv(self, models, factory=None):
        return conv.Char(required=self.required)

    def create_widget(self, model,factory=None):
        return widgets.TextInput()


class IF_String(IF_Simple):
    min_length=0
    max_length=250
    regex = None

    def create_conv(self, models, factory=None):
        return convs.Char(convs.length(self.min_length, self.max_length),
                          required=self.required,
                          regex=self.regex)


class IF_Text(IF_String):
    min_length=0
    max_length=2000

    def create_widget(self, models, factory=None):
        return widgets.Textarea()


class IF_Title(IF_Text):
    name = 'title'
    label = u'Заголовок'
    max_length = 1000
    required = True
    initial = ''

    def create_conv(self, models, factory=None):
        return convs.Char(convs.length(0, max_length),
                          NoUpperConv,
                          StripTrailingDotConv,
                          required=self.required,)


class IF_Int(IF_Simple):

    def create_conv(self, models, factory=None):
        return convs.Int(required=self.required)


class IF_Id(IF_Int):
    name = 'id'
    label = u'ID'
    permissions = 'r'


class IF_HiddenId(IF_Id):
    permissions = 'rw'
    def create_widget(self, factory, models):
        return widgets.HiddenInput


class IF_Bool(IF_Simple):

    def create_conv(self, models, factory=None):
        return convs.Bool(required=self.required)

    def create_widget(self, models, factory=None):
        return widgets.CheckBox()


class IF_Select(IF_Simple):
    choices = None

    def create_conv(self, models, factory=None):
        if self.choices:
            choices = self.choices
        else:
            assert factory and hasattr(factory, 'model'), \
               'Field name=%s: You must specify choices or factory.model' % \
                                                                     self.name
            model = getattr(models, factory.model)
            choices = getattr(model, '%s_choices' % self.name)
        return convs.EnumChoice(conv=convs.Char(required=self.required),
                                choices=choices,
                                required=self.required)

    def create_widget(self, models, factory=None):
        if 'w' in self.permissions:
            return widgets.Select()
        else:
            return widgets.Select(template="widgets/readonly_select",
                                  classname="small")


class IF_StreamSelect(IF_Simple):
    model = None
    stream_name = None
    multiple = False
    allow_create = False
    allow_select = True
    allow_delete = True
    unshift = False
    condition = None
    default_filters = {}
    ordered = True
    rel = None
    conv = convs.Int

    def create_conv(self, models, factory=None):
        model_conv = convs.ModelChoice(
                                model=getattr(models, self.model),
                                conv=self.conv(required=self.required),
                                condition=self.condition,
                                required=self.required)
        if self.multiple:
            return convs.ListOf(model_conv, required=self.required)
        else:
            return model_conv

    def create_widget(self, models, factory=None):
        return widgets.PopupStreamSelect(
            stream_name=self.stream_name,
            allow_create=self.allow_create,
            allow_select=self.allow_select,
            allow_delete=self.allow_delete,
            sortable=self.ordered,
            unshift=self.unshift,
            default_filters=self.default_filters,
            rel=self.rel,
        )


class IF_File(IF_Simple):

    def create_field(self, models, factory=None):
        return fields.AjaxFileField(self.name,
                             conv=self.create_conv(models, factory),
                             widget=self.create_widget(models, factory),
                             label=self.label,)

    def create_conv(self, models, factory=None):
        return fields.AjaxFileField.conv(required=self.required)

    def create_widget(self, model, factory=None):
        return fields.AjaxFileField.widget


class IF_Img(IF_Simple):
    show_thumbnail = False
    show_size = False
    crop = False

    def create_field(self, models, factory=None):
        return fields.AjaxImageField(self.name,
                             conv=self.create_conv(models, factory),
                             widget=self.create_widget(models, factory),
                             label=self.label,
                             show_thumbnail=self.show_thumbnail,
                             show_size=self.show_size,
                             crop=self.crop,
                             )

    def create_conv(self, models, factory=None):
        return fields.AjaxImageField.conv(required=self.required)

    def create_widget(self, model, factory=None):
        return fields.AjaxImageField.widget


class IF_Block(IF_Base):
    fields = []

    def item_field(self, fields_dict, models, factory=None):
        block_fields_dict = OrderedDict()
        for field in self.fields:
            field.item_field(block_fields_dict, models, factory)
        fields_dict[self.name] = fields.FieldBlock(self.label,
                                            fields=block_fields_dict.values())


class IF_DateTime(IF_Base):

    def item_field(self, fields_dict, models, factory=None):
        fields_dict[self.name] = fields.SplitDateTimeField(self.name,
                                                           label=self.label)

class IF_List(IF_Base):
    model = None
    fields = [IF_Id(), IF_Title(required=False),]

    def item_field(self, fields_dict, models, factory=None):
        list_fields_dict = OrderedDict()
        for field in [if_hidden_id] + self.fields:
            field.item_field(list_fields_dict, models, factory)
        fieldset = fields.FieldSet(None,
            conv=convs.ModelDictConv(model=getattr(models, self.model)),
            fields=list_fields_dict.values(),
        )
        fields_dict[self.name] = fields.FieldList(self.name,
                                                  order=True,
                                                  label=self.label,
                                                  field=fieldset,)

if_title = IF_Title('title')
if_id = IF_Id()
if_hidden_id = IF_HiddenId()
