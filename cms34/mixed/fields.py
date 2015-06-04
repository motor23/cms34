# -*- coding: utf8 -*-
from datetime import datetime

from ..utils import prop_getter
from ..model import (
    MF_String,
    MF_Text,
    MF_Int,
    MF_Bool,
    MF_Id,
    MF_M2ORelation,
    MF_M2MRelation,
    MF_Parent,
    MF_File,
    MF_Img,
    MF_DateTime,
    MF_Enum,
    MF_Html,
    MF_ExpHtml,
    MF_List,
)
from ..stream import (
    LF_String,
    LF_Id,
    LF_Img,
    LF_Relation,
    LF_DateTime,
    LF_Container,
    LF_EnumImg,
    FF_TextSearch,
    FF_Int,
    FF_Id,
    FF_Select,
    FF_TabSelect,
    FF_DateTimeFromTo,
    FF_StreamSelect,
    IF_String,
    IF_Text,
    IF_Int,
    IF_Bool,
    IF_Id,
    IF_Select,
    IF_StreamSelect,
    IF_File,
    IF_Img,
    IF_Block,
    IF_DateTime,
    IF_Html,
    IF_ExpHtml,
    IF_List,
    lf_tree_expand,
)

__all__ = (
    'XF_Base',
    'XF_String',
    'XF_Slug',
    'XF_Text',
    'XF_Title',
    'XF_Lead',
    'XF_Int',
    'XF_Order',
    'XF_Bool',
    'XF_Id',
    'XF_Select',
    'XF_Type',
    'XF_TypeImg',
    'XF_StreamSelect',
    'XF_Parent',
    'XF_List',
    'XF_Block',
    'XF_File',
    'XF_Img',
    'XF_DateTime',
    'XF_Dt',
    'XF_PublishDt',
    'XF_Html',
    'XF_ExpHtml',
    'XF_Body',
    'XF_TreeTitle',
    'XB_Object',
    'XB_Content',
    'xf_slug',
    'xf_title',
    'xf_tree_title',
    'xf_lead',
    'xf_id',
    'xf_order',
    'xf_type',
    'xf_parent',
    'xf_dt',
    'xf_publish_dt',
    'xf_html',
    'xf_body',
    'xf_file',
    'xb_object',
)


class XF_Base(object):
    name = None
    label = None
    permissions = "rw"

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def model_register(self, factory=None, register=None):
        raise NotImplementedError()

    def model_field(self, fields_dict, models, factory=None):
        raise NotImplementedError()

    def list_field(self, fields_dict):
        raise NotImplementedError()

    def filter_field(self, fields_dict, models, factory=None):
        raise NotImplementedError('field name=%s' % self.name)

    def filter_form(self, fields_dict, models, factory=None):
        pass

    def filter_defaults(self, fields_dict, models, form, factory=None):
        pass

    def item_field(self, fields_dict, models, factory=None):
        raise NotImplementedError()

    def item_form(self, fields_dict, models, factory=None):
        raise NotImplementedError()

    def sort_field(self, fields_dict, models, factory=None):
        pass


class XF_Simple(XF_Base):
    initial = None
    required = False
    sortable = False

    def __init__(self, name=None, **kwargs):
        XF_Base.__init__(self, name, **kwargs)

    def _model_field(self, factory=None):
        raise NotImplementedError(
            'cls=%s, name=%s' % (self.__class__, self.name))

    def _list_field(self):
        return LF_String(self.name, label=self.label)

    def _filter_field(self, models, factory=None):
        raise NotImplementedError(
            'cls=%s, name=%s' % (self.__class__, self.name))

    def _item_field(self, models, factory=None):
        raise NotImplementedError(
            'cls=%s, name=%s' % (self.__class__, self.name))

    def model_register(self, factory=None, register=None):
        field = self._model_field(factory)
        field.model_register(factory, register)

    def model_field(self, fields_dict, models, factory=None):
        field = self._model_field(factory)
        field.model_field(fields_dict, models, factory)

    def list_field(self, fields_dict):
        field = self._list_field()
        field.list_field(fields_dict)

    def filter_field(self, fields_dict, models, factory=None):
        field = self._filter_field(models, factory)
        field.filter_field(fields_dict, models, factory)

    def filter_form(self, fields_dict, models, factory=None):
        field = self._filter_field(models, factory)
        field.filter_form(fields_dict, models, factory)

    def filter_defaults(self, defaults_dict, models, form, factory=None):
        field = self._filter_field(models, factory)
        field.filter_defaults(defaults_dict, models, form, factory)

    def item_field(self, fields_dict, models, factory=None):
        field = self._item_field(models, factory)
        field.item_field(fields_dict, models, factory)

    def item_form(self, fields_dict, models, factory=None):
        field = self._item_field(models, factory)
        field.item_form(fields_dict, models, factory)

    def sort_field(self, fields_dict, models, factory=None):
        if self.sortable:
            fields_dict[self.name] = self.name


class XF_String(XF_Simple):
    max_length = 255
    min_length = 0
    regex = None
    sortable = True

    def _model_field(self, factory=None):
        return MF_String(self.name,
                         length=self.max_length,
                         default=self.initial)

    def _filter_field(self, models, factory=None):
        return FF_TextSearch(self.name, label=self.label)

    def _item_field(self, models, factory=None):
        return IF_String(self.name,
                         label=self.label,
                         max_length=self.max_length,
                         min_length=self.min_length,
                         initial=self.initial,
                         required=self.required,
                         permissions=self.permissions,
                         regexp=self.regex)

    def _list_field(self):
        return LF_String(self.name, label=self.label)


class XF_Slug(XF_String):
    required = True
    min_length = 2
    regex = r'^[A-Za-z][A-Za-z0-9_-]+$'
    sortable = True


class XF_Text(XF_String):
    max_length = 2000
    min_length = 0

    def _model_field(self, factory=None):
        return MF_Text(self.name,
                       default=self.initial, )

    def _item_field(self, models, factory=None):
        return IF_Text(self.name,
                       label=self.label,
                       max_length=self.max_length,
                       min_length=self.min_length,
                       initial=self.initial,
                       permissions=self.permissions,
                       required=self.required)


class XF_Title(XF_Text):
    name = 'title'
    label = u'Заголовок'
    required = True
    sortable = True


class XF_TreeTitle(XF_Title):
    list_fields = []

    def _list_field(self):
        return LF_Container('%s_container' % self.name,
                            label=self.label,
                            fields=self.container_list_fields(),
                            )

    def container_list_fields(self):
        return [
            lf_tree_expand,
            LF_String(self.name,
                      label=self.label,
                      ),
        ]


class XF_Lead(XF_Text):
    name = 'lead'
    label = u'Лид'


class XF_Slug(XF_String):
    name = 'slug'
    label = u'Слаг'
    required = True


class XF_Int(XF_Simple):
    sortable = True

    def _model_field(self, factory=None):
        return MF_Int(self.name,
                      default=self.initial, )

    def _filter_field(self, models, factory=None):
        return FF_Int(self.name, label=self.label)

    def _item_field(self, models, factory=None):
        return IF_Int(self.name,
                      label=self.label,
                      initial=self.initial,
                      permisssions=self.permissions,
                      required=self.required, )


class XF_Order(XF_Int):
    name = 'order'
    label = u'Вес'
    initial = 100


class XF_Bool(XF_Simple):
    sortable = True

    def _model_field(self, factory=None):
        return MF_Bool(self.name,
                       default=self.initial, )

    def _item_field(self, models, factory=None):
        return IF_Bool(self.name,
                       label=self.label,
                       initial=self.initial,
                       permissions=self.permissions,
                       required=self.required, )


class XF_Id(XF_Simple):
    name = 'id'
    label = u'ID'
    autoincrement = True
    sortable = True

    def _model_field(self, factory=None):
        return MF_Id(self.name,
                     default=self.initial,
                     autoincrement=self.autoincrement)

    def _list_field(self):
        return LF_Id(self.name,
                     label=self.label)

    def _filter_field(self, models, factory=None):
        return FF_Id(self.name,
                     label=self.label)

    def _item_field(self, models, factory=None):
        return IF_Id(self.name,
                     label=self.label, )


class XF_Select(XF_Simple):
    choices = None

    def _model_field(self, factory=None):
        return MF_Enum(self.name, choices=self.choices)

    def _list_field(self):
        return LF_String('%s_name' % self.name, label=self.label)

    def _filter_field(self, models, factory=None):
        return FF_Select(self.name,
                         label=self.label,
                         choices=self.choices)

    def _item_field(self, models, factory=None):
        return IF_Select(self.name,
                         label=self.label,
                         choices=self.choices,
                         permissions=self.permissions,
                         required=self.required)


class XF_Type(XF_Select):
    name = 'type'
    label = u'Тип'
    permissions = "r"

    def _filter_field(self, models, factory=None):
        return FF_TabSelect(self.name, label=self.label, choices=self.choices)

    def filter_defaults(self, defaults_dict, models, form, factory=None):
        filter_value = form.python_data.get(self.name)
        if filter_value:
            defaults_dict[self.name] = filter_value
        else:
            field = self._filter_field(models, factory)
            defaults_dict[self.name] = field.get_choices(models, factory)[0][0]


class XF_TypeImg(XF_Type):
    img_url_teplate = LF_EnumImg.img_url_template

    def _list_field(self):
        return LF_EnumImg(self.name,
                          label=self.label,
                          img_url_template=self.img_url_template,
                          )


class XF_StreamSelect(XF_Simple):
    model = None
    stream_name = None
    multiple = False
    allow_create = False
    allow_select = True
    allow_delete = True
    inshift = False
    condition = None
    default_filters = {}
    ordered = False
    rel = None
    required = False

    def _model_field(self, factory=None):
        if self.multiple:
            return MF_M2MRelation(
                self.name,
                ordered=self.ordered,
                remote_cls_name=self.model,
            )
        else:
            return MF_M2ORelation(
                self.name,
                remote_cls_name=self.model,
            )

    def _item_field(self, models, factory=None):
        return IF_StreamSelect(
            self.name,
            label=self.label,
            model=self.model,
            stream_name=self.stream_name,
            multiple=self.multiple,
            allow_create=self.allow_create,
            allow_select=self.allow_select,
            allow_delete=self.allow_delete,
            inshift=self.inshift,
            condition=self.condition,
            default_filters=self.default_filters,
            ordered=self.ordered,
            rel=self.rel,
            required=self.required,
        )

    def _filter_field(self, models, factory=None):
        return FF_StreamSelect(
            self.name,
            label=self.label,
            model=self.model,
            stream_name=self.stream_name,
            multiple=self.multiple,
            condition=self.condition,
            default_filters=self.default_filters,
        )

    def _list_field(self):
        return LF_Relation(self.name,
                           label=self.label,
                           multiple=self.multiple, )


class XF_Parent(XF_Simple):
    name = 'parent'
    label = u'Родитель'
    model = None
    get_model = prop_getter('model', 'model')
    stream_name = None
    get_stream_name = prop_getter('stream_name', 'name')
    default_filters = {}
    rel = None

    def _model_field(self, factory=None):
        return MF_Parent(self.name)

    def _item_field(self, models, factory=None):
        return IF_StreamSelect(
            self.name,
            label=self.label,
            model=self.get_model(factory),
            stream_name=self.get_stream_name(factory),
            default_filters=self.default_filters,
            rel=self.rel,
        )


class XF_Group(XF_Base):
    fields = []
    model_fields = property(lambda self: self.fields)
    list_fields = property(lambda self: self.fields)
    filter_fields = property(lambda self: self.fields)
    item_fields = property(lambda self: self.fields)
    sort_fields = property(lambda self: self.fields)

    def model_register(self, factory=None, register=None):
        for field in self.model_fields:
            field.model_register(factory, register)

    def model_field(self, fields_dict, models, factory=None):
        for field in self.model_fields:
            field.model_field(fields_dict, models, factory)

    def list_field(self, fields_dict):
        for field in self.list_fields:
            field.list_field(fields_dict)

    def filter_field(self, fields_dict, models, factory=None):
        for field in self.filter_fields:
            field.filter_field(fields_dict, models, factory)

    def filter_form(self, fields_dict, models, factory=None):
        for field in self.filter_fields:
            field.filter_form(fields_dict, models, factory)

    def filter_defaults(self, defaults_dict, models, form, factory=None):
        for field in self.filter_fields:
            field.filter_defaults(defaults_dict, models, form, factory)

    def item_field(self, fields_dict, models, factory=None):
        for field in self.item_fields:
            field.item_field(fields_dict, models, factory)

    def item_form(self, fields_dict, models, factory=None):
        for field in self.item_fields:
            field.item_form(fields_dict, models, factory)

    def sort_field(self, fields_dict, models, factory=None):
        for field in self.sort_fields:
            field.sort_field(fields_dict, models, factory)


class XF_Block(XF_Group):
    def item_field(self, fields_dict, models, factory=None):
        field = IF_Block(self.name,
                         label=self.label,
                         fields=self.item_fields)
        field.item_field(fields_dict, models, factory)


class XF_File(XF_Simple):
    name = 'file'
    label = u'Фаил'

    def _model_field(self, factory=None):
        return MF_File(self.name)

    def list_field(self, fields_dict):
        pass

    def _item_field(self, models, factory=None):
        return IF_File(self.name, label=self.label)


class XF_Img(XF_Simple):
    image_sizes = None
    resize = None
    fill_from = None

    show_thumbnail = False
    show_size = False
    crop = False

    def _model_field(self, factory=None):
        return MF_Img(self.name,
                      image_sizes=self.image_sizes,
                      fill_from=self.fill_from,
                      resize=self.resize,
                      )

    def _list_field(self):
        return LF_Img(self.name, label=self.label)

    def _item_field(self, models, factory=None):
        return IF_Img(self.name,
                      label=self.label,
                      show_thumbnail=self.show_thumbnail,
                      crop=self.crop,
                      )


class XF_DateTime(XF_Simple):
    format = "%d-%m-%Y %H:%M"
    initial = datetime.now
    sortable = True

    def _model_field(self, factory=None):
        return MF_DateTime(self.name,
                           default=self.initial)

    def _list_field(self):
        return LF_DateTime(self.name,
                           label=self.label,
                           format=self.format)

    def _filter_field(self, models, factory=None):
        return FF_DateTimeFromTo(self.name,
                                 label=self.label)

    def _item_field(self, models, factory=None):
        return IF_DateTime(self.name,
                           label=self.label,
                           format=self.format)


class XF_Dt(XF_DateTime):
    name = 'dt'
    label = u'Дата'


class XF_PublishDt(XF_DateTime):
    name = 'publish_dt'
    label = u'Дата публикации'


class XF_Html(XF_Simple):
    name = 'html'
    label = u'Текст'

    allowed_elements = IF_Html.allowed_elements
    allowed_protocols = IF_Html.allowed_protocols
    allowed_attributes = IF_Html.allowed_attributes
    button_blocks = IF_Html.button_blocks
    stylesheets = IF_Html.stylesheets

    def _model_field(self, factory=None):
        return MF_Html(self.name)

    def _item_field(self, models, factory=None):
        return IF_Html(self.name,
                       label=self.label,
                       allowed_elements=self.allowed_elements,
                       allowed_protocols=self.allowed_protocols,
                       allowed_attributes=self.allowed_attributes,
                       button_blocks=self.button_blocks,
                       stylesheets=self.stylesheets,
                       )


class XF_ExpHtml(XF_Html):
    allowed_elements = IF_ExpHtml.allowed_elements
    allowed_protocols = IF_ExpHtml.allowed_protocols
    allowed_attributes = IF_ExpHtml.allowed_attributes
    button_blocks = IF_ExpHtml.button_blocks
    stylesheets = IF_ExpHtml.stylesheets

    def _model_field(self, factory=None):
        return MF_ExpHtml(self.name)

    def _item_field(self, models, factory=None):
        return IF_ExpHtml(self.name,
                          label=self.label,
                          allowed_elements=self.allowed_elements,
                          allowed_protocols=self.allowed_protocols,
                          allowed_attributes=self.allowed_attributes,
                          button_blocks=self.button_blocks,
                          stylesheets=self.stylesheets,
                          )


class XF_Body(XF_ExpHtml):
    name = 'body'


class XF_List(XF_Simple):
    name = 'links'
    label = u'xxxx'
    fields = []
    model = None
    parent_model = None

    def get_template_locals(self, factory=None):
        l = {'name': self.name}
        if factory:
            l['factory_model'] = factory.main_factory.model
        return l

    def get_model(self, factory=None):
        return self.model % self.get_template_locals(factory)

    def _model_field(self, factory=None):
        return MF_List(self.name,
                       remote_cls_name=self.get_model(factory),
                       fields=self.fields, )

    def _item_field(self, models, factory=None):
        return IF_List(self.name,
                       label=self.label,
                       model=self.get_model(factory),
                       fields=self.fields, )


xf_slug = XF_Slug()
xf_title = XF_Title()
xf_tree_title = XF_TreeTitle()
xf_lead = XF_Lead()
xf_id = XF_Id()
xf_order = XF_Order()
xf_parent = XF_Parent()
xf_type = XF_Type()
xf_dt = XF_Dt()
xf_publish_dt = XF_PublishDt()
xf_html = XF_Html()
xf_body = XF_Body()
xf_file = XF_File()


class XB_Object(XF_Block):
    name = 'object_block'
    label = u'Объект'
    fields = [xf_id]


class XB_Content(XF_Block):
    name = 'content'
    label = u'Контент'


xb_object = XB_Object()
