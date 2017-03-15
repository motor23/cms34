# -*- coding: utf8 -*-
from lxml import html
from lxml.etree import XMLSyntaxError

from iktomi.utils import cached_property

from cms34.model import hybrid_factory_method
from cms34.model import (
    ModelFactory,
    mf_id,
    mf_title,
    mf_body,
)


class MFY_Page(ModelFactory):
    title = u'Страница'
    model = 'Page'

    fields = [
        mf_id,
        mf_body,
    ]

    @hybrid_factory_method.model
    @cached_property
    def hanging_file_blocks(self):
        """
        Return list of file blocks attached to event but not inserted in body.
        """
        tag_name = 'iktomi_files'
        body = self.body.markup
        try:
            tree = html.fromstring(body)
        except XMLSyntaxError:
            return []

        expr = "//{}".format(tag_name)
        tags = tree.xpath(expr)
        inserted_file_block_ids = [int(tag.attrib['item_id']) for tag in tags]
        return [block for block in self.files_blocks if
                block.id not in inserted_file_block_ids]

    @hybrid_factory_method.model
    @cached_property
    def hanging_link_blocks(self):
        """
        Return list of link blocks attached to event but not inserted in body.
        """
        tag_name = 'iktomi_doclink'
        body = self.body.markup
        try:
            tree = html.fromstring(body)
        except XMLSyntaxError:
            return []

        expr = "//{}".format(tag_name)
        tags = tree.xpath(expr)
        inserted_link_block_ids = [int(tag.attrib['item_id']) for tag in tags]

        return [block for block in self.links_blocks if
                block.id not in inserted_link_block_ids]
