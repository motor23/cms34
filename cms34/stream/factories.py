# -*- coding: utf8 -*-
from collections import OrderedDict

from iktomi.cms.stream import FilterForm
from iktomi.cms.publishing.i18n_stream import PublishStream
from iktomi.cms.forms import ModelForm

def dict_to_register(streams_dict):
    def register(name, stream):
        streams_dict[name] = stream
    return register


class ListFieldsFactory(object):

    fields = None

    def __init__(self, fields=None, **kwargs):
        self.fields = fields or self.fields
        assert self.fields, \
               u'You must specify "fields" property, cls=%s' % self.__class__

    def get_fields(self):
        fields_dict = OrderedDict()
        for field in self.fields:
            field.list_field(fields_dict)
        return fields_dict


class FormFactoryBase(object):

    fields = []
    name = 'Form'
    stream_factory = None

    def __init__(self, fields=None, stream_factory=None, **kwargs):
        self.fields = (fields is not None) and fields or self.fields
        assert self.fields is not None, \
               u'You must specify "fields" property, cls=%s' % self.__class__
        self.stream_factory = stream_factory or self.stream_factory

    def __call__(self, env, *args, **kwargs):
        return self.get_form(env, *args, **kwargs)(env, *args, **kwargs)

    def load_initial(self, env, item, initial, *args, **kwargs):
        return self.get_form(env, initial, item, *args, **kwargs)\
                   .load_initial(env, item, initial, *args, **kwargs)

    def get_form(self, env, initial, item, *args, **kwargs):
        raise NotImplementedError


class FormFactory(FormFactoryBase):

    bases = (ModelForm,)

    def get_form(self, env, *args, **kwargs):
        return type(self.name, self.bases, self.get_form_dict(env.models))

    def get_form_dict(self, models):
        raise NotImplementedError


class FilterFormFactory(FormFactory):

    bases = (FilterForm,)
    name = 'FilterForm'

    def get_form_dict(self, models):
        form_dict = OrderedDict()
        fields_dict = OrderedDict()
        for field in self.fields:
            field.filter_field(fields_dict, models,  self.stream_factory)
        form_dict['fields_dict'] = fields_dict
        form_dict['fields'] = fields_dict.values()

        def defaults(form):
            defaults_dict = {}
            for field in self.fields:
                field.filter_defaults(
                    defaults_dict,
                    models,
                    form,
                    self.stream_factory)
            return defaults_dict
        form_dict['defaults'] = defaults

        for field in self.fields:
            field.filter_form(form_dict, models, self.stream_factory)
        return form_dict


class ItemFormFactory(FormFactory):

    bases = (ModelForm,)
    name = 'ItemForm'

    def get_form_dict(self, models):
        form_dict = OrderedDict()
        fields_dict = OrderedDict()
        for field in self.fields:
            field.item_field(fields_dict, models, self.stream_factory)
        form_dict['fields_dict'] = fields_dict
        form_dict['fields'] = fields_dict.values()
        for field in self.fields:
            field.item_form(form_dict, models, self.stream_factory)
        return form_dict


class FormFactoryDispatcher(FormFactoryBase):

    field_name = None
    form_factory = None

    def __init__(self, fields=None, stream_factory=None):
        assert isinstance(fields, dict)
        FormFactoryBase.__init__(self, fields, stream_factory)

    def get_form(self, env, initial, item, *args, **kwargs):
        value = getattr(item, self.field_name)
        return self.form_factory(self.fields[value],
                                 stream_factory=self.stream_factory,)\
                   .get_form(env, initial, item, *args, **kwargs)


class TypedItemFormFactory(FormFactoryDispatcher):
    field_name = 'type'
    form_factory = ItemFormFactory


class StreamFactory(object):

    model = None
    register = None
    name = None
    stream_bases = (PublishStream,)
    fields = []
    list_fields = None
    filter_fields = None
    item_fields = None
    permissions = {'wheel':'rwxdcp'}
    limit = None
    list_fields_factory = ListFieldsFactory
    filter_form_factory = FilterFormFactory
    item_form_factory = ItemFormFactory
    plugins = []
    common_plugins = []

    class Cfg(object): pass

    def __init__(self, register, name=None, **kwargs):
        self.register = register or self.register
        assert self.register, \
               u'You must specify register param, cls=%s' % self.__class__
        self.name = name or self.name
        assert self.name, \
               u'You must specify name param, cls=%s' % self.__class__
        self.__dict__.update(kwargs)
        self.plugins = map(lambda x:x(self), self.plugins+self.common_plugins)
        self.cfg = self.create_config()
        register(self.name, self.create_stream())

    def create_config(self):
        print self.name
        cfg = self.Cfg()
        cfg.title = self.title
        cfg.permissions = self.permissions
        cfg.limit = self.limit
        cfg.Stream = self.create_stream_cls()
        cfg.Model = self.model
        cfg.list_fields = self.create_list_fields()
        cfg.FilterForm = self.create_filter_form()
        cfg.ItemForm = self.create_item_form()
        for plugin in self.plugins:
            plugin.create_config(self, cfg)
        return cfg

    def create_stream_cls(self):
        return type('Stream', self.stream_bases, {})

    def create_stream(self):
        return self.cfg.Stream(self.name, self.cfg)

    def create_list_fields(self):
        factory = self.list_fields_factory
        fields = (self.list_fields is None) and self.fields or self.list_fields
        for plugin in self.plugins:
            factory, fields = plugin.create_list_fields(factory, fields)
        return factory(fields).get_fields()

    def create_filter_form(self):
        factory = self.filter_form_factory
        fields = (self.filter_fields is None) and self.fields \
                                              or self.filter_fields
        for plugin in self.plugins:
            factory, fields = plugin.create_item_form(factory, fields)
        return factory(fields, stream_factory=self)

    def create_item_form(self):
        factory = self.item_form_factory
        fields = (self.item_fields is None) and self.fields or self.item_fields
        for plugin in self.plugins:
            factory, fields = plugin.create_item_form(factory, fields)
        return factory(fields, stream_factory=self)

    @property
    def main_factory(self):
        return self

