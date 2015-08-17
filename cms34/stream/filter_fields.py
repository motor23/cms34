# -*- coding: utf8 -*-
from collections import OrderedDict

from iktomi.forms import Field
from iktomi.cms.forms import convs, widgets, fields
from iktomi.cms.forms.fields import SortField

__all__ = (
    'FF_Base',
    'FF_Text',
    'FF_Int',
    'FF_TextSearch',
    'FF_Id',
    'FF_Select',
    'FF_TabSelect',
    'FF_DateTimeFromTo',
    'FF_StreamSelect',
    'FF_Sort',
    'ff_id',
)

class FF_Base(object):
    label = None
    name = None

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def filter_field(self, fields_dict, models, factory=None):
        fields_dict[self.name] = self.create_field(models, factory)

    def filter_form(self, form_dict, models, factory=None):
        pass

    def filter_defaults(self, defaults_dict, models, form, item=None, factory=None):
        pass

    def create_field(self, models, factory=None):
        return Field(
            self.name,
            conv=self.create_conv(models, factory),
            widget=self.create_widget(models, factory),
            label=self.label,
            filter_query=self.filter_query,
        )

    def create_conv(self, models, factory=None):
        raise NotImplementedError()

    def create_widget(self, model, factory=None):
        raise NotImplementedError()

    def filter_query(self, query, field, filter_value):
        return field.form.filter_by_default(query, field, filter_value)


class FF_Text(FF_Base):

    def create_conv(self, models, factory=None):
        return convs.Char()

    def create_widget(self, model, factory=None):
        return widgets.TextInput()


class FF_Int(FF_Text):

    def create_conv(self, models, factory=None):
        return convs.Int()


class FF_TextSearch(FF_Text):

    def filter_query(self, query, field, filter_value):
        model_field = getattr(field.form.model, self.name)
        for value in filter_value.split():
            query = query.filter(model_field.like("%" + value + "%"))
        return query


class FF_Id(FF_Text):
    name = 'id'
    label = 'ID'

    def create_widget(self, models, factory=None):
        return widgets.TextInput(template="widgets/id_field",
                                 classname="small")


class FF_Select(FF_Base):
    choices = None

    def create_conv(self, models, factory=None):
        return convs.EnumChoice(conv=convs.Char(),
                                choices=self.get_choices(models, factory))

    def create_widget(self, models, factory=None):
        return widgets.Select()

    def get_choices(self, models, factory=None):
        if self.choices is not None:
            return self.choices
        assert factory is not None
        model = getattr(models, factory.model)
        return getattr(model, '%s_choices' % self.name)


class FF_TabSelect(FF_Select):
    null_label = u'Все'

    def create_widget(self, models, factory=None):
        return widgets.TabSelect(
                null_label=self.null_label,
                classname='hidden',
        )


class FF_DateTimeFromTo(FF_Base):

    def filter_field(self, fields_dict, models, factory=None):
        fields_dict[self.name] = fields.DateFromTo(self.name, label=self.label)


class FF_StreamSelect(FF_Base):
    model = None
    label = None
    stream_name = None
    multiple = False
    default_filters = {}
    conv = convs.Int

    def create_conv(self, models, factory=None):
        model_conv = convs.ModelChoice(
                                model=getattr(models, self.model),
                                conv=self.conv(),
                                condition=self.condition,)
        if self.multiple:
            return convs.ListOf(model_conv)
        else:
            return model_conv

    def create_widget(self, models, factory=None):
        return widgets.PopupStreamSelect(
            stream_name=self.stream_name,
            default_filters=self.default_filters,
        )


class FF_Sort(FF_Base):

    name = 'sort'
    fields = []
    initial = None

    def create_field(self, models, factory=None):
        return SortField(self.name,
            choices=self.get_choices(models, factory),
            initial=self.get_initial(models, factory),
            )

    def get_choices(self, models, factory=None):
        result = OrderedDict()
        for field in self.fields:
            if isinstance(field, tuple):
                result[field[0]] = field[1]
            else:
                field.sort_field(result, models, factory)
        return result.items()

    def get_initial(self, models, factory=None):
        if self.initial is None:
            if self.fields:
                return self.get_choices(models, factory)[0][0]
            else:
                return 'id'
        if isinstance(self.initial, basestring):
            return self.initial
        else:
            result = OrderedDict()
            self.initial.sort_field(result, models, factory)
            return result.keys()[0]


ff_id = FF_Id()


