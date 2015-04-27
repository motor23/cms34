# -*- coding: utf8 -*-
from ...mixed.fields import (
    XF_StreamSelect,
    XF_Select,
    XF_TypeImg,
    XF_Block,
    XF_File,
    XF_Img,
    xf_file,
)

class XF_MediaSelect(XF_StreamSelect):
    name = 'media'
    label = u'Главный медиа объект'
    model = 'Media'
    stream_name = 'multimedia'

class XF_PhotoSelect(XF_StreamSelect):
    name = 'photo'
    label = u'Фото'
    model = 'Photo'
    stream_name = 'multimedia'
    default_filters = {'type': 'photo'}

class XF_PhotosSelect(XF_StreamSelect):
    name = 'photos'
    label = u'Фото'
    model = 'Photo'
    stream_name = 'multimedia'
    multiple = True
    default_filters = {'type': 'photo'}

class XF_VideoSelect(XF_StreamSelect):
    name = 'video'
    label = u'Видео'
    model = 'Video'
    stream_name = 'multimedia'
    default_filters = {'type': 'vide'}

class XF_PhotoSetSelect(XF_StreamSelect):
    name = 'photoset'
    label = u'Фотосет'
    model = 'PhotoSet'
    stream_name = 'multimedia'
    default_filters = {'type': 'photoset'}

class XF_FileSelect(XF_StreamSelect):
    name = 'file'
    label = u'Фаил'
    model = 'File'
    stream_name = 'multimedia'
    default_filters = {'type': 'file'}

class XF_MediasSelect(XF_StreamSelect):
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


class XF_MediaTypeImg(XF_TypeImg):
    img_url_template = '/cms34-static/img/multimedia/%(value)s.png'


class XF_ImgOrig(XF_Img):
    name = 'img_orig'
    label = u'Фото в исходном разрешении'
    required = True


class XF_Sd(XF_File):
    name = 'sd'
    label=u'Видео sd'

class XF_Hd(XF_File):
    name = 'hd'
    label=u'Видео hd'

class XF_PosterOrig(XF_Img):
    name='poster_orig'
    label=u'Постер в исходном разрешении'


xf_media_select = XF_MediaSelect()
xf_photo_select = XF_PhotoSelect()
xf_photos_select = XF_PhotosSelect()
xf_video_select = XF_VideoSelect()
xf_photoset_select = XF_PhotoSetSelect()
xf_medias_select = XF_MediasSelect()
xf_aspect = XF_Aspect()
xf_media_type_img = XF_MediaTypeImg()
xf_img_orig = XF_ImgOrig()
xf_sd = XF_Sd()
xf_hd = XF_Hd()
xf_poster_orig = XF_PosterOrig()


class XB_Media(XF_Block):
    name = 'media_block'
    label = u'Мультимедия'
    item_fields = [
        xf_medias_select,
    ]

class XB_Photos(XF_Block):
    name = 'photos_block'
    label = u'Фото'
    item_fields = [
        xf_photos_select,
    ]

class XB_PhotoUpload(XF_Block):
    name = 'photo_upload_block'
    label = u'Изображения'
    item_fields = [
        xf_img_orig,
    ]

class XB_FileUpload(XF_Block):
    name = 'file_upload_block'
    label = u'Фаил'
    item_fields = [
        xf_file,
    ]

class XB_VideoUpload(XF_Block):
    name = 'video_block'
    label = u'Видео'
    item_fields = [
        xf_sd,
        xf_hd,
    ]

class XB_PosterUpload(XF_Block):
    name = 'poster_upload_block'
    label = u'Постер'
    item_fields = [
        xf_poster_orig,
    ]

xb_media = XB_Media()
xb_photos = XB_Photos()
xb_photo_upload = XB_PhotoUpload()
xb_file_upload = XB_FileUpload()
xb_video_upload = XB_VideoUpload()
xb_poster_upload = XB_PosterUpload()

