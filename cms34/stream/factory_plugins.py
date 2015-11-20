# -*- coding: utf8 -*-
#
# Stream Factory Plugin => (SFP_%s)
#

from iktomi.cms.ajax_file_upload import (
    StreamFileUploadHandler,
    StreamImageUploadHandler,
)
from iktomi.cms.edit_log.views import EditLogHandler

from .html_body_handlers import (
    HtmlBodyHandler,
)
from .stream_actions import PreviewAction
from .stream_handlers import RecursiveDeleteFlagItemHandler


class SFP_Base(object):
    def __init__(self, factory=None, **kwargs):
        self.factory = factory
        self._kwargs = kwargs
        self.__dict__.update(kwargs)

    def __call__(self, factory):
        return self.__class__(factory=factory, **self._kwargs)

    def create_filter_form(self, factory, fields):
        return factory, fields

    def create_item_form(self, factory, fields):
        return factory, fields

    def create_list_fields(self, factory, fields):
        return factory, fields

    def create_config(self, factory, cfg):
        pass

    def create_stream_cls(self, stream_cls):
        return stream_cls


class SFP_Tree(SFP_Base):
    delete_handler_cls = RecursiveDeleteFlagItemHandler

    def create_config(self, factory, cfg):
        cfg.modify_items = self.modify_items

    def create_stream_cls(self, stream_cls):
        """
        Override base `delete` action in Stream.
        """
        filtered_actions = [action for action in stream_cls.core_actions if
                            action.action != self.delete_handler_cls.action]
        stream_cls.core_actions = filtered_actions + [self.delete_handler_cls()]
        return stream_cls

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
        root_items = filter(lambda item: item.parent == parent, items)
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


class SFP_HtmlBody(SFP_Base):
    handler_cls = HtmlBodyHandler

    def create_config(self, factory, cfg):
        cfg.Stream.actions = cfg.Stream.actions + [self.handler_cls()]


class SFP_ChildFactories(SFP_Base):
    def create_config(self, factory, cfg):
        item_fields = dict(factory.item_fields)
        for _factory in factory.child_factories:
            item_fields[_factory.name] = _factory.item_fields
        factory.item_fields = item_fields


class SFP_Action(SFP_Base):
    def __init__(self, action, factory=None, **kwargs):
        kwargs['action'] = action
        SFP_Base.__init__(self, factory, **kwargs)

    def create_stream_cls(self, stream_cls):
        stream_cls.actions = stream_cls.actions + [self.action]
        return stream_cls


def SFP_Preview(**kwargs):
    return SFP_Action(PreviewAction(**kwargs))


def SFP_EditLog(**kwargs):
    return SFP_Action(EditLogHandler(**kwargs))
