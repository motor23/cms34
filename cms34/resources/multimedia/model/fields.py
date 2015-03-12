from std.model.fields import (
    MF_M2MRelation,
    MF_M2ORelation,
)

mf_photo = MF_M2ORelation('photo', remote_cls_name='Photo')

mf_video = MF_M2ORelation('video', remote_cls_name='Video')

mf_photoset = MF_M2ORelation('photoset', remote_cls_name='PhotoSet')

mf_file = MF_M2ORelation('file', remote_cls_name='File')

mf_main_media = MF_M2ORelation('main_media', remote_cls_name='Media')

mf_media = MF_M2MRelation('media', remote_cls_name='Media', ordered=True)


