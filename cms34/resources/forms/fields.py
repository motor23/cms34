# -*- coding: utf-8 -*-
from cms34.model import hybrid_factory_method
from iktomi.utils import cached_property
from cms34.mixed.fields import (
    XF_Title,
    XF_String,
    XF_Select,
    XF_List,
    xf_title,
    XF_Block,
    XF_StreamSelect,
    XF_Type,
    XF_Bool,
    MF_List as MF_ListBase,
)
from .front.fields import (
    CF_FieldBlock
)


class XF_FieldName(XF_String):
    name = 'name'
    label = u'Имя поля (на латинице)'
    required = True


class XF_FieldSize(XF_Select):
    name = 'size'
    label = u'Размер поля'

    choices = [
        ('small', u'Маленькое'),
        ('medium', u'Среднее'),
        ('large', u'Большое'),
    ]


class XF_FieldType(XF_Type):
    name = 'type'
    label = u'Тип поля'
    permissions = 'rw'
    # Choices are defined in factory


class XF_Required(XF_Bool):
    name = 'required'
    label = u'Обязательное поле'
    initial = True


class XF_AnswerOption(XF_Title):
    name = 'title'
    label = u'Вариант ответа'
    required = True


xf_required = XF_Required()
xf_answer_option = XF_AnswerOption()


class XF_OptionsList(XF_List):
    name = 'options'
    label = u'Варианты ответа'
    model = 'OptionChoice'

    fields = [
        xf_answer_option,
    ]


xf_field_name = XF_FieldName()
xf_field_size = XF_FieldSize()
xf_field_type = XF_FieldType()
xf_options_list = XF_OptionsList()


class XF_FormFieldSelect(XF_StreamSelect):
    name = 'fields'
    model = 'FormField'
    stream_name = 'form_fields'
    multiple = True
    allow_create = True
    allow_select = True
    allow_delete = True
    ordered = True


xf_form_field_select = XF_FormFieldSelect()


# Hack to assign model property to remote model of XF_BlockList
class MF_List(MF_ListBase):
    class remote_factory_cls(MF_ListBase.remote_factory_cls):
        @hybrid_factory_method.model
        @cached_property
        def front_view_cls(self):
            return CF_FieldBlock


class XF_BlockList(XF_List):
    name = 'form'
    label = u'Блоки формы'
    model = 'FormBlockList'

    fields = [
        xf_title,
        xf_form_field_select,
    ]

    def _model_field(self, factory=None):
        return MF_List(self.name,
                       remote_cls_name=self.get_model(factory),
                       fields=self.fields, )


xf_form_block_list = XF_BlockList()


class XB_FormFieldBlocks(XF_Block):
    name = 'form_block'
    label = u'Форма'

    fields = [
        xf_form_block_list,
    ]


xb_form_blocks = XB_FormFieldBlocks()
