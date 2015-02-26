# -*- coding: utf8 -*-
from ...mixed.fields import (
    XF_StreamSelect,
    XF_Select,
)

class XF_Media(XF_StreamSelect):
    name = 'media'
    label = u'Медия'
    model = 'Media'
    stream_name = 'multimedia'

class XF_Photo(XF_StreamSelect):
    name = 'photo'
    label = u'Фото'
    model = 'Photo'
    stream_name = 'multimedia'

class XF_Video(XF_StreamSelect):
    name = 'video'
    label = u'Видео'
    model = 'Video'
    stream_name = 'multimedia'

class XF_PhotoSet(XF_StreamSelect):
    name = 'photoset'
    label = u'Фотосет'
    model = 'PhotoSet'
    stream_name = 'multimedia'

class XF_File(XF_StreamSelect):
    name = 'file'
    label = u'Фаил'
    model = 'File'
    stream_name = 'multimedia'

class XF_Medias(XF_StreamSelect):
    name = 'medias'
    label = u'Медия'
    model = 'Media'
    stream_name = 'multimedia'
    multiple = True
    ordered = True


class XF_Aspect(XF_Select):
    name = 'aspect'
    choices = (('4_3', u'4:3'),
               ('16_9', u'16:9'),)


xf_media = XF_Media()
xf_photo = XF_Photo()
xf_video = XF_Video()
xf_photoset = XF_PhotoSet()
xf_medias = XF_Medias()
xf_aspect = XF_Aspect()

