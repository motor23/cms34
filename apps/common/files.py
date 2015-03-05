import os
import logging
from sqlalchemy.orm import object_session
from iktomi.unstable.db.files import FileManager as FileManagerBase
from iktomi.cms.publishing.model import _FrontReplicated, _WithState


logger = logging.getLogger(__name__)


class SymlinkableEventHandlers(object):

    # def before_insert(self, mapper, connection, target):
    #     super(SymlinkableEventHandlers, self).before_update(mapper, connection, target)
    #     self.update_symlinks(target)

    def before_update(self, mapper, connection, target):
        super(SymlinkableEventHandlers, self).before_update(mapper, connection, target)
        self.update_symlinks(target)

    def update_symlinks(self, target):
        if isinstance(target, _FrontReplicated):
            if isinstance(target, _WithState):
                session = object_session(target)
                attr = getattr(type(target), self.prop.key)
                file = getattr(target, self.prop.key)
                if file is not None:
                    file_manager = session.find_file_manager(attr)
                    if target.public:
                        file_manager.create_symlink(file)
                    else:
                        file_manager.delete_symlink(file)


class FileManager(FileManagerBase):

    def __init__(self, transient_root=None, persistent_root=None,
                       transient_url=None, persistent_url=None,
                       public_root=None):
        self.transient_root = transient_root
        self.persistent_root = persistent_root
        self.transient_url = transient_url
        self.persistent_url = persistent_url
        self.public_root = public_root

    def create_symlink(self, file):
        source_path = os.path.normpath(file.path)
        target_path = os.path.join(self.public_root, file.name)
        target_path = os.path.normpath(target_path)
        target_directory = os.path.dirname(target_path)
        source_path_rel = os.path.relpath(source_path, os.path.split(target_path)[0])
        if not os.path.isdir(target_directory):
            os.makedirs(target_directory)
        if os.path.islink(target_path):
            logger.info('Unlinking existing %s', target_path)
            os.unlink(target_path)
        logger.info('Symlinking %s to %s', source_path_rel, target_path)
        os.symlink(source_path_rel, target_path)

    def delete_symlink(self, file):
        path = os.path.join(self.public_root, file.name)
        if os.path.isfile(path):
            logger.info('Unlinking %s', path)
            os.unlink(path)
