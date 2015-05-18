# -*- coding: utf8 -*-
from cms34.model.factories import (
    ModelFactory,
    MFP_Types,
    hybrid_factory_method,
)
from cms34.mixed.fields import (
    xf_id,
    xf_dt,
    xf_publish_dt,
    xf_title,
    xf_file,
)
from .fields import (
    xf_img_orig,
    xf_photos_select,
    xf_sd,
    xf_hd,
    xf_poster_orig,
    xf_aspect,
    xf_poster_4_3,
    xf_poster_16_9,
)


class MFY_Photo(ModelFactory):
    model = 'Photo'
    title = u'Фото'
    base_path = 'photo'
    fields = [
        xf_id,
        xf_img_orig,
    ]

class MFY_PhotoSet(ModelFactory):
    model = 'PhotoSet'
    title = u'Фотолента'
    fields = [
        xf_id,
        xf_photos_select,
    ]

class MFY_Video(ModelFactory):
    model = 'Video'
    title = u'Видео'
    base_path = 'video'
    fields = [
        xf_id,
        xf_sd,
        xf_hd,
        xf_poster_orig,
        xf_aspect,
        xf_poster_4_3,
        xf_poster_16_9,
    ]

class MFY_File(ModelFactory):
    model = 'File'
    title = u'Файл'
    base_path = 'files'
    fields = [
        xf_id,
        xf_file,
    ]

class MFY_Media(ModelFactory):

    model = 'Media'
    title = u'Медиа'
    plugins = [MFP_Types]
    types = [
        ('photo', MFY_Photo),
        ('video', MFY_Video),
        ('photoset', MFY_PhotoSet),
        ('file', MFY_File),
    ]

    fields = [
        xf_id,
        xf_dt,
        xf_publish_dt,
        xf_title,
    ]

    @hybrid_factory_method.model
    @property
    def admin_preview(obj):
        prop = getattr(obj.factory, 'admin_preview_property', None)
        if prop:
            return getattr(obj, prop)
        else:
            return None

