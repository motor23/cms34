# -*- coding: utf8 -*-
import types
from collections import OrderedDict

from iktomi.utils import cached_property, cached_class_property
from sqlalchemy import ForeignKeyConstraint

from ..utils import prop_getter
from .fields import MF_Enum

def decorator_to_registry(dec, **kwargs):
    def register(name, constructor, bases):
        def func(models):
            locals().update(constructor(models))
        func.func_name = name
        dec(*bases, **kwargs)(func)
    return register


class HybridFactoryMethod(object):
    def __init__(self, factory_method=None, model_method=None):
        self.factory_method = factory_method
        self.model_method = model_method

    def factory(self, factory_method):
        return self.__class__(factory_method, self.model_method)

    def model(self, model_method):
        return self.__class__(self.factory_method, model_method)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not self.factory_method:
            raise NotImplementedError()
        return self.factory_method.__get__(instance, owner)

hybrid_factory_method = HybridFactoryMethod()


class ModelFactory(object):

    fields = []
    register = None
    title = None
    bases = []
    rel_cls_bases = []
    plugins = []
    id_field_name = 'id'

    def __init__(self, register=None,
                       bases=None,
                       rel_cls_bases=None,
                       plugins=None,
                       main_factory=None):
        self.register = register or self.register
        assert self.register, \
               u'You must specify register param, cls=%s' % self.__class__
        self.bases = bases or self.bases
        self.rel_cls_bases = rel_cls_bases or self.rel_cls_bases
        plugins = plugins or self.plugins
        self.plugins = [plugin(self) for plugin in plugins]
        self.main_factory = main_factory or self  # For List model template
        for field in self.fields:
            field.model_register(self)
        self.register(self.name, self.get_model_dict, self.bases)
        for plugin in self.plugins:
            plugin.register()

    def get_model_dict(self, models):
        model_dict = OrderedDict({
            'factory': self,
            'models': models,
            '__title__': self.title,
        })
        for field in self.fields:
            field.model_field(model_dict, models, self)
        for prop_name in dir(self.__class__):
            prop = getattr(self.__class__, prop_name)
            if isinstance(prop, HybridFactoryMethod) and prop.model_method:
                model_dict[prop_name] = prop.model_method
        for plugin in self.plugins:
            plugin.get_model_dict(model_dict, models)
        return model_dict

    @cached_class_property #XXX
    def model(cls):
        return cls.__name__

    @cached_class_property #XXX
    def name(cls):
        return cls.model


class ModelFactoryPlugin(object):

    def __init__(self, factory=None, **kwargs):
        self.factory = factory
        self.kwargs = kwargs
        self.__dict__.update(kwargs)

    def __call__(self, factory):
        return self.__class__(factory, **self.kwargs)

    def get_model_dict(self, model_dict, models): pass
    def register(self): pass


class I18nPlugin(ModelFactoryPlugin):

    def get_model_dict(self, model_dict, models):
        if models.lang != models.main_lang:
            model_dict.setdefault('__table_args__', ())
            remote = '%sRu.%s' % (self.factory.name,
                                  self.factory.id_field_name)
            model_dict['__table_args__']+= \
                     (ForeignKeyConstraint([self.factory.id_field_name],
                      [remote]),)


class TypesPlugin(ModelFactoryPlugin):

    class TypePlugin(ModelFactoryPlugin):

        parent_factory = None
        get_parent_factory = prop_getter('parent_factory')
        identity = None
        get_identity = prop_getter('identity')

        def get_model_dict(self, model_dict, models):
            parent_factory = self.get_parent_factory()
            mapper_args = model_dict.setdefault('__mapper_args__', {})
            mapper_args['polymorphic_identity'] = self.get_identity()

            model_dict.setdefault('__table_args__', ())
            remote_model = getattr(models, parent_factory.name)
            remote_id = getattr(remote_model,
                                parent_factory.id_field_name)
            model_dict['__table_args__']+= \
                     (ForeignKeyConstraint([self.factory.id_field_name],
                                           [remote_id]),)

    type_field_name = 'type'

    def __init__(self, factory):
        ModelFactoryPlugin.__init__(self, factory)
        self.types = getattr(self.factory, 'types', None)
        assert self.types, \
               u'You must specify types param, factory=%s' % factory

    def get_model_dict(self, model_dict, models):
        self.type_field(self.types).model_field(model_dict, models, self.factory)
        mapper_args = model_dict.setdefault('__mapper_args__', {})
        mapper_args['polymorphic_on'] = self.type_field_name

        def __new__(cls, **initial):
            identity = initial.get(self.type_field_name)
            if identity:
                for type_identity, type in self.factory.types:
                    if type_identity==identity:
                        cls = getattr(models, type.name)
                        break;
                else:
                    raise Exception('Model="%s": Unknown type %s' % \
                                       (cls, initial[self.type_field_name]))
            return super(getattr(models, self.factory.name), cls).__new__(cls)
        model_dict['__new__']=__new__

    def type_field(self, types):
        return MF_Enum(self.type_field_name,
                       choices=map(lambda x: (x[0], x[1].title), types))

    def register(self):
        for identity, type_factory in self.types:
            type_plugin = self.TypePlugin(
                parent_factory=self.factory,
                identity=identity)
            type_factory(
                self.factory.register,
                bases=[self.factory.name] + type_factory.bases,
                rel_cls_bases=self.factory.rel_cls_bases,
                plugins=[type_plugin] + type_factory.plugins,
            )


class SingleTableTypesPlugin(TypesPlugin):
    class TypePlugin(TypesPlugin.TypePlugin):
        def get_model_dict(self, model_dict, models):
            mapper_args = model_dict.setdefault('__mapper_args__', {})
            mapper_args['polymorphic_identity'] = self.identity
            model_dict['__tablename__'] = None


class AddFieldsPlugin(ModelFactoryPlugin):
    fields = None
    get_fields = prop_getter('fields')

    def get_model_dict(self, model_dict, models):
        fields = self.get_fields()
        for field in fields:
            field.model_field(model_dict, models, self.factory)

