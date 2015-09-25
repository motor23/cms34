# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sphinxqla import types
from cms34.model import ModelFactory
from cms34.mixed import xf_id

__all__ = [
    'search_index_dispatcher',
]

Base = declarative_base()


class Material(Base):
    __abstract__ = True

    material_types = (
        ('event', u'События'),
        ('theme', u'Темы'),
        ('person', u'Персоны'),
        ('org', u'Организации'),
    )

    document_id = Column(types.Integer, primary_key=True)
    section_id = Column(types.Integer)
    parent_id = Column(types.Integer)
    dt = Column(types.Timestamp, nullable=True)
    model_name = Column(types.String, nullable=True)
    section = Column(types.String, nullable=True)
    type = Column(types.String, nullable=True)


class CollectionDispatcher(object):
    def __init__(self, *collection_classes):
        self._collection_classes = collection_classes
        self._models = {}

    def __call__(self, env):
        for cls in self._collection_classes:
            model_name = cls.__name__
            if model_name not in self._models:
                model = type(model_name, (cls,),
                             {'__tablename__': env.cfg.SPHINX_COLLECTION_NAME})
                self._models[model_name] = model
        return self

    def __getattr__(self, item):
        return self._models[item]


search_index_dispatcher = CollectionDispatcher(Material)


class MFY_SearchSection(ModelFactory):
    title = u'Поиск'
    model = 'SearchSection'

    fields = [
        xf_id,
    ]
