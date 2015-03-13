# -*- coding: utf8 -*-
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
    Enum,
    Boolean,
    VARBINARY as VarBinary,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    ForeignKey,
)

from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from iktomi.utils import cached_property
from iktomi.unstable.db.files import PersistentFile
from iktomi.cms.publishing.files import (
    PublicatedImageProperty,
    PublicatedFileProperty,
)
from ..utils import prop_getter

__all__ = (
    'MF_Base',
    'MF_Int',
    'MF_Id',
    'MF_LangId',
    'MF_Bool',
    'MF_DateTime',
    'MF_String',
    'MF_Text',
    'MF_Enum',
    'MF_Type',
    'MF_O2MRelation',
    'MF_Parent',
    'MF_M2ORelation',
    'MF_M2MRelation',
    'MF_File',
    'MF_Img',
    'mf_id',
    'mf_lang_id',
    'mf_dt',
    'mf_publish_dt',
    'mf_title',
    'mf_lead',
    'mf_slug',
    'mf_order',
    'mf_parent',
)


class MF_Base(object):

    name = None
    primary_key = False
    nullable = True
    default = None

    cls_name = None
    get_cls_name = prop_getter('cls_name', 'name')

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def model_field(self, fields, models, factory=None):
        fields.update(self.get_dict(models, factory))
        mapper_args = fields.setdefault('__mapper_args__', {})
        mapper_args.update(self.get_mapper_args(models, factory))
        table_args = fields.get('__table_args__', ())
        fields['__table_args__'] = table_args + \
                                   self.get_table_args(models, factory)

    def model_register(self, factory=None, register=None):
        if register is None and factory is not None:
            register = factory.register
        assert register, \
               u'You must specify factory o register param'
        self.register(factory, register)

    def get_dict(self, models, factory=None): return {}

    def get_mapper_args(self, models, factory=None): return {}

    def get_table_args(self, models, factory=None): return ()

    def register(self, factory, register): pass


class MF_Int(MF_Base):

    autoincrement=False

    def get_dict(self, models, factory=None):
        return {self.name: Column(Integer,
                                  autoincrement=self.autoincrement,
                                  nullable=self.nullable,
                                  default=self.default,
                                  )}


class MF_Id(MF_Base):
    name = 'id'
    primary_key = True
    field_cls = MF_Int
    autoincrement = True

    def get_dict(self, models, factory=None):
        field = self.field_cls(self.name,
                               primary_key=self.primary_key,
                               autoincrement=self.autoincrement,)
        return field.get_dict(models, factory)

    def get_table_args(self, models, factory=None):
        result = []
        if self.primary_key:
            result.append(PrimaryKeyConstraint(self.name))
        return tuple(result)


class MF_LangId(MF_Id):

    def get_table_args(self, models, factory=None):
        args = super(MF_LangId, self).get_table_args(models, factory)
        if models.lang != models.main_lang:
            cls_name = self.get_cls_name(factory)
            remote = '%sRu.%s' % (cls_name, self.name)
            args = args+ (ForeignKeyConstraint([self.name], [remote]),)
        return args


class MF_Bool(MF_Base):

    def get_dict(self, models, factory=None):
        return {self.name: Column(Boolean,
                                  nullable=self.nullable,
                                  default=self.default,
                                  )}


class MF_DateTime(MF_Base):
    name = 'dt'
    default = datetime.now

    def get_dict(self, models, factory=None):
        dt = Column(DateTime,
                    nullable=self.nullable,
                    default=self.default,
                    index=True)
        return {self.name: dt}


class MF_String(MF_Base):
    default = ''
    length = 255
    def get_dict(self, models, factory=None):
        string = Column(String(self.length),
                        nullable=self.nullable,
                        default=self.default,)
        return {self.name: string}


class MF_Text(MF_Base):
    default = ''
    def get_dict(self, models, factory=None):
        text = Column(Text,
                      nullable=self.nullable,
                      default=self.default)
        return {self.name: text}


class MF_Enum(MF_Base):
    choices = None
    nullable = True

    def get_dict(self, models, factory=None):
        if self.choices is None:
            factory_property = '%s_choices' % self.name
            if factory:
                type_choices = getattr(factory, factory_property, None)
            else:
                type_choices = None
            assert type_choices is not None, \
                   u'Field name=%s: You must specify choices property or '\
                    'factory.%s property' % (self.name, factory_property)
        else:
            type_choices = self.choices

        type = Column(Enum(*dict(type_choices).keys()),
                      nullable=self.nullable)

        @cached_property
        def type_name(_self):
            value = getattr(_self, self.name)
            if value is not None:
                return dict(type_choices)[value]
            else:
                return None

        return {
            self.name: type,
            '%s_choices' % self.name: type_choices,
            '%s_name' % self.name: type_name,
        }


class MF_Type(MF_Enum):
    name = 'type'

class MF_M2ORelation(MF_Base):

    ondelete = 'set null'
    nullable = True
    remote_cls_name = None
    get_remote_cls_name = prop_getter('remote_cls_name')

    def get_dict(self, models, factory=None):
        remote_cls_name = self.get_remote_cls_name(factory)
        remote_cls = getattr(models, remote_cls_name)
        field_id = Column(Integer,
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


class MF_Parent(MF_M2ORelation):

    name = 'parent'

    @property
    def remote_cls_name(self):
        assert False, 'Use get remote cls name, field=%s' % self.name

    def get_remote_cls_name(self, factory=None):
        return self.get_cls_name(factory)

    def get_dict(self, models, factory=None):
        #XXX This is must be plugin?
        model_dict = MF_M2ORelation.get_dict(self, models, factory)

        @cached_property
        def parents(self):
            result = []
            if self.parent_id is None:
                return result
            parent = self.parent
            while parent:
                result.append(parent)
                parent = parent.parent
            return result

        @cached_property
        def tree_level(self):
            return len(self.parents) + 1

        #XXX Why this is here?
        @cached_property
        def tree_path(self):
            slugs = [self.slug] + [item.slug for item in self.parents]
            slugs.reverse()
            return '/' + '/'.join(slugs)

        return dict(model_dict,
                    parents=parents,
                    tree_level=tree_level,
                    tree_path=tree_path,)


class MF_O2MRelation(MF_Base):

    ordered = False
    cascade = 'all, delete-orphan'
    remote_cls_name = None
    get_remote_cls_name = prop_getter('remote_cls_name')

    def get_dict(self, models, factory=None):
        remote_cls_name = self.get_remote_cls_name(factory)
        remote_cls = getattr(models, remote_cls_name)
        kwargs = {}
        if self.ordered:
            kwargs['collection_class'] = ordering_list('order')
            kwargs['order_by'] = [remote_cls.order]
        if self.cascade:
            kwargs['cascade'] = self.cascade
        field = relation(remote_cls, **kwargs)
        return {
            self.name: field,
        }


class MF_M2MRelation(MF_Base):

    ordered = False
    rel_cls_name = None
    rel_cls_bases = None
    get_rel_cls_bases = prop_getter('rel_cls_bases', 'rel_cls_bases')
    remote_cls_name = None
    get_remote_cls_name = prop_getter('remote_cls_name')
    ordered = False


    def get_dict(self, models, factory=None):
        rel_name = "%s_relation" % self.name
        rel_cls_name = self.get_rel_cls_name(factory)
        rel_cls = getattr(models, rel_cls_name)
        remote_cls_name = self.get_remote_cls_name(factory)
        kwargs = {}
        if self.ordered:
            kwargs['order_by'] = rel_cls.order
            kwargs['collection_class'] = ordering_list('order')

        rel = relation(rel_cls,
                       passive_deletes=None,
                       cascade='all, delete-orphan',
                       **kwargs)

        def creator(item):
            rel_cls = getattr(models, rel_cls_name)
            return rel_cls(**{remote_cls_name.lower():item})
        field = association_proxy(rel_name, remote_cls_name.lower(),
                                  creator=creator)
        return {
            rel_name: rel,
            self.name: field,
        }

    def register(self, factory, register):
        def get_rel_cls_dict(models):
            return self.get_rel_cls_dict(models, factory)
        register(self.get_rel_cls_name(factory),
                 get_rel_cls_dict,
                 self.get_rel_cls_bases(factory),
                 )
        fields = self.get_rel_cls_fields(factory)
        for field in fields:
            field.model_register(factory, register)


    def get_rel_cls_name(self, factory=None):
        if self.rel_cls_name is not None:
            return self.rel_cls_name
        return '%s_%s' % (self.get_cls_name(factory),
                          self.get_remote_cls_name())

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
            MF_M2ORelation(
                remote_cls_name.lower(),
                remote_cls_name = remote_cls_name,
                nullable = False,
                ondelete = 'cascade',
                primary_key = True,
            ),
        ]

    def get_rel_cls_dict(self, models, factory=None):
        fields = self.get_rel_cls_fields(factory)
        cls_dict = {}
        for field in fields:
            field.model_field(cls_dict, models, factory)
        if self.ordered:
            mf_order.model_field(cls_dict, models, factory)
        return cls_dict


class MF_File(MF_Base):

    base_path = None
    get_base_path = prop_getter('base_path', 'base_path')

    class _File(PersistentFile):

        @cached_property
        def extension(self):
            ext = self.ext
            if ext.startswith('.'):
                ext = ext[1:]
            return ext

    def get_dict(self, models, factory=None):
        base_path = self.get_base_path(factory)
        file_name = Column(VarBinary(250))
        file = PublicatedFileProperty(
            file_name,
            persistent_cls=self._File,
            name_template=('%s/%s/{random}' % (base_path, self.name)),
            cache_properties={'extension': '%s_ext' % self.name},
        )
        file_ext = Column(String(10))
        return {
            '%s_name' % self.name: file_name,
            '%s_ext' % self.name: file_ext,
            self.name: file,
        }


class MF_Img(MF_Base):

    image_sizes = None
    resize = None
    fill_from = None
    base_path = None
    get_base_path = prop_getter('base_path', 'base_path')

    def get_dict(self, models, factory=None):
        base_path = self.get_base_path(factory)
        img_name = Column(VarBinary(250))
        img = PublicatedImageProperty(img_name,
            image_sizes=self.image_sizes,
            resize=self.resize,
            fill_from=self.fill_from,
            name_template=('%s/%s/{random}' % (base_path, self.name))
        )
        return {
            '%s_name' % self.name: img_name,
            self.name: img,
        }


mf_id = MF_Id('id')
mf_lang_id = MF_LangId('id')
mf_dt = MF_DateTime('dt')
mf_publish_dt = MF_DateTime('publish_dt')
mf_title = MF_String('title')
mf_lead = MF_Text('lead')
mf_slug = MF_String('slug')
mf_order = MF_Int('order')
mf_parent = MF_Parent('parent')
