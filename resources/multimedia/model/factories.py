# -*- coding: utf8 -*-
from ....model.factories import (
    ModelFactory,
    TypesPlugin,
    hybrid_factory_method,
)
from ....model.fields import (
    mf_id,
    mf_dt,
    mf_publish_dt,
    mf_title,
    MF_File,
    MF_Img,
    MF_M2MRelation,
)


class Photo(ModelFactory):
    title = u'Фото'
    base_path = 'photo'
    fields = [
        mf_id,
        MF_Img('img_orig'),
    ]

class PhotoSet(ModelFactory):
    title = u'Фотолента'
    fields = [
        mf_id,
        MF_M2MRelation('photos',
                       remote_cls_name='Photo',
                       ordered=True),
    ]

class Video(ModelFactory):
    title = u'Видео'
    base_path = 'video'
    fields = [
        mf_id,
        MF_File('sd'),
        MF_File('hd'),
        MF_File('wmv'),
        MF_Img('preview_orig'),
    ]

class File(ModelFactory):
    title = u'Файл'
    base_path = 'files'
    fields = [
        mf_id,
        MF_File('file'),
    ]

class Media(ModelFactory):

    title = u'Медиа'
    plugins = [TypesPlugin]
    types = [
        ('photo', Photo),
        ('video', Video),
        ('photoset', PhotoSet),
        ('file', File),
    ]

    fields = [
        mf_id,
        mf_dt,
        mf_publish_dt,
        mf_title,
    ]

    @hybrid_factory_method.model
    @property
    def admin_preview(obj):
        prop = getattr(obj.factory, 'admin_preview_property', None)
        if prop:
            return getattr(obj, prop)
        else:
            return None

