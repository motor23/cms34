from sqlalchemy.orm import sessionmaker
from iktomi.db.sqla import multidb_binds
from iktomi.unstable.db.sqla.files import filesessionmaker


def binded_sessionmaker(databases,
                        engine_params=None,
                        session_params=None):

    engine_params = engine_params or {}
    binds = multidb_binds(databases,
                          package='models',
                          engine_params=engine_params)

    session_params = session_params or {}
    session_params.setdefault('autoflush', False)
    return sessionmaker(binds=binds, **session_params)


def binded_filesessionmaker(databases,
                            engine_params=None,
                            session_params=None,
                            default_file_manager=None,
                            file_managers=None):
    return filesessionmaker(
        binded_sessionmaker(databases,
                            engine_params=engine_params,
                            session_params=session_params),
        default_file_manager,
        file_managers=file_managers)


#def create_session_maker(cfg, de
#    return  binded_filesessionmaker(cfg.DATABASES,
#                                   engine_params=cfg.DATABASE_PARAMS,
#                                   default_file_manager=_file_manager,
#                                   file_managers={
#                                       models.shared.metadata: shared_file_manager,
#                                   })


