# -*- coding: utf8 -*-
#
# Stream Factory Plugin => (SFP_%s)
#

from iktomi.cms.ajax_file_upload import (
    StreamFileUploadHandler,
    StreamImageUploadHandler,
)

class SFP_Base(object):

    def __init__(self, factory=None, **kwargs):
        self.factory = factory
        self.__dict__.update(kwargs)

    def __call__(self, factory):
        return self.__class___(factory)

    def create_filter_form(self, factory, fields):
        return factory, fields

    def create_item_form(self, factory, fields):
        return factory, fields

    def create_list_fields(self, factory, fields):
        return factory, fields

    def create_config(self, factory, cfg):
        pass


class SFP_Tree(SFP_Base):

    def create_config(self, factory, cfg):
        cfg.modify_items = self.modify_items

    def modify_items(self, items):
        tree = self._get_child_items(None, items)
        for item in items:
            if item not in tree:
                item.tree_level = 0
                tree.append(item)
        return tree

    def _get_child_items(self, parent, items):
        # build tree
        result = []
        root_items = filter(lambda item: item.parent==parent, items)
        for root_item in list(root_items):
            result.append(root_item)
            child_items = self._get_child_items(root_item, items)
            root_item.has_childs = bool(child_items)
            result += child_items
        return result


class SFP_FileUpload(SFP_Base):

    def create_config(self, factory, cfg):
        cfg.Stream.actions = cfg.Stream.actions + [StreamFileUploadHandler()]


class SFP_ImageUpload(SFP_Base):

    def create_config(self, factory, cfg):
        cfg.Stream.actions = cfg.Stream.actions + [StreamImageUploadHandler()]


