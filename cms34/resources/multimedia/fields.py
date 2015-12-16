# -*- coding: utf8 -*-
from cms34.mixed import XF_Block
from cms34.resources.tags.fields import xf_tags
from cms34.resources.sections.fields import xf_section
from iktomi.unstable.utils.image_resizers import (
    ResizeCrop,
)
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
    label = u'Медиа'
    model = 'Media'
    stream_name = 'multimedia'
    multiple = True
    ordered = True


class XF_Aspect(XF_Select):
    name = 'aspect'
    label = u'Соотношение сторон'
    required = True
    choices = (('4_3', u'4:3'),
               ('16_9', u'16:9'),)


class XF_MediaTypeImg(XF_TypeImg):
    img_url_template = '/cms34-static/img/multimedia/%(value)s.png'


class XF_ImgOrig(XF_Img):
    name = 'img_orig'
    label = u'Фото в исходном разрешении (Не более 5000×5000)'
    required = True


class XF_Sd(XF_File):
    name = 'sd'
    label = u'Видео sd'


class XF_Hd(XF_File):
    name = 'hd'
    label = u'Видео hd'


class XF_PosterOrig(XF_Img):
    name = 'poster_orig'
    label = u'Постер в исходном разрешении'


class XF_Poster4_3(XF_Img):
    label = u'Постер 4:3'
    name = 'poster_4_3'
    image_sizes = (640, 480)
    resize = ResizeCrop()
    fill_from = 'poster_orig'
    required = True
    show_thumbnail = True
    show_size = True
    crop = True


class XF_Poster16_9(XF_Img):
    label = u'Постер 16:9'
    name = 'poster_16_9'
    image_sizes = (640, 360)
    resize = ResizeCrop()
    fill_from = 'poster_orig'
    required = True
    show_thumbnail = True
    show_size = True
    crop = True


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
xf_poster_4_3 = XF_Poster4_3()
xf_poster_16_9 = XF_Poster16_9()


class XB_Media(XF_Block):
    name = 'media_block'
    label = u'Мультимедиа'
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
        xf_aspect,
        xf_sd,
        xf_hd,
    ]


class XB_PosterUpload(XF_Block):
    name = 'poster_upload_block'
    label = u'Постер'
    item_fields = [
        xf_poster_orig,
        xf_poster_4_3,
        xf_poster_16_9,
    ]


class XB_MediaSectionTags(XF_Block):
    name = 'tags_block'
    label = u'Классификаторы'
    fields = [
        xf_tags,
    ]


class XB_MediaItemTags(XB_MediaSectionTags):
    fields = [
        xf_section,
        xf_tags,
    ]


xb_media = XB_Media()
xb_photos = XB_Photos()
xb_photo_upload = XB_PhotoUpload()
xb_file_upload = XB_FileUpload()
xb_video_upload = XB_VideoUpload()
xb_poster_upload = XB_PosterUpload()
xb_media_section_tags = XB_MediaSectionTags()
xb_media_item_tags = XB_MediaItemTags()
