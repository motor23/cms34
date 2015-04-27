# -*- coding: utf-8 -*-
from ...stream import (
    StreamFactory,
    TypedItemFormFactory,
    SFP_FileUpload,
    SFP_ImageUpload,
)
from ...mixed import (
    XF_Block,
    XF_Img,
    xf_title,
    xf_lead,
    xf_dt,
    xf_publish_dt,
    xb_object,
)
from .fields import (
    xf_media_type_img,
    xb_photos,
    xb_photo_upload,
    xb_file_upload,
    xb_poster_upload,
    xb_video_upload,
)


class XB_Main(XF_Block):
    name = 'media_block'
    label = u'Медиа'
    list_fields = (
        xf_media_type_img,
        xf_title,
        xf_dt,
        xf_publish_dt,
    )
    sort_fields = (
        xf_dt,
        xf_publish_dt,
    )
    filter_fields = (
        xf_media_type_img,
        xf_title,
        xf_dt,
        xf_publish_dt,
    )
    item_fields = (
        xf_media_type_img,
        xf_dt,
        xf_publish_dt,
        xf_title,
    )


xb_main = XB_Main()


class SFY_Multimedia(StreamFactory):
    name = 'multimedia'
    model = 'Media'
    title = u'Медиа'
    limit = 40
    item_form_factory = TypedItemFormFactory
    plugins = [SFP_FileUpload, SFP_ImageUpload]

    permissions = {
        'wheel':'rwxdcp',
        'editor':'rwxdcp',
    }

    list_fields = [
        xb_object,
        XF_Img('admin_preview', label=u'Превью'),
        xb_main,
    ]
    filter_fields = [
        xb_object,
        xb_main,
    ]
    fields = [
        xb_object,
        xb_main,
    ]
    sort_fields = list_fields
    item_fields = {
        'photo': fields + [xb_photo_upload],
        'photoset': fields + [xb_photos],
        'video': fields + [xb_poster_upload, xb_video_upload],
        'file': fields + [xb_file_upload],
    }
