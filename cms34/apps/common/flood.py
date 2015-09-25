# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def check_flood(env, activity, update):
    """
    Important: you are responsible to commit after calling this function.
    """
    if not env.cfg.FLOOD_PROTECTION_ENABLED:
        return
    flood_model = env.flood_models.FloodProtection
    flooder = env.db.query(flood_model) \
        .filter_by(activity_type=activity,
                   ip=env.request.remote_addr).first()
    if not flooder:
        if not update:
            return
        flooder = flood_model(ip=env.request.remote_addr,
                              activity_type=activity)
        # need this to init fields of new users
        flooder.update_activity(env.cfg.FLOOD_PROTECTION)
        env.db.add(flooder)
        env.db.commit()
        return

    allowed_at = flooder.check_flood()
    if not allowed_at:
        flooder.update_activity(env.cfg.FLOOD_PROTECTION)
    else:
        logger.info("flooding from %s. allowed at: %s", flooder.ip, allowed_at)
    return allowed_at
