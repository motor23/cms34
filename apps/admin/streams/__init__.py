# -*- coding: utf-8 -*-

from iktomi.cms.stream_app import Streams
from iktomi.cms.publishing.i18n_stream import I18nPublishStream

from cms34.stream import dict_to_register

streams_tree = [
    'admins',
]

streams = Streams.from_tree(streams_tree, __package__)

register = dict_to_register(streams)

