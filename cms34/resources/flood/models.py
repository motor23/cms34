# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from cms34.model import ModelFactory, hybrid_factory_method
from cms34.mixed import xf_id

from .fields import (
    xf_ip,
    xf_last_activity,
    xf_activity_weight,
    xf_activity_type,
)

FLOOD_PROTECTION_DEFAULTS = (0, 60, 1, 10 * 60)


class MFY_FloodProtection(ModelFactory):
    model = 'FloodProtection'
    title = u'Защита от флуда'

    fields = [
        xf_id,
        xf_ip,
        xf_last_activity,
        xf_activity_weight,
        xf_activity_type,
    ]

    @hybrid_factory_method.model
    def update_activity(self, FLOOD_PROTECTION):
        now = datetime.now()
        free_tries, init_value, multiplier, timeout = \
            FLOOD_PROTECTION.get(self.activity_type) or \
            FLOOD_PROTECTION.get('default') or \
            FLOOD_PROTECTION_DEFAULTS

        # reset condition: new user or more then timeout since last activity
        if (self.id is None) or \
                (self.last_activity < now - timedelta(seconds=timeout)):
            if free_tries:
                self.activity_weight = -free_tries
            else:
                self.activity_weight = init_value
            self.last_activity = now
            return

        # some strange numbers here but this should work properly
        if self.activity_weight < -1:
            self.activity_weight += 1
        elif self.activity_weight <= 0:
            self.activity_weight = init_value
        else:
            self.activity_weight *= multiplier

        if self.activity_weight > timeout:
            self.activity_weight = timeout

        self.last_activity = now

    @hybrid_factory_method.model
    def check_flood(self):
        now = datetime.now()

        if self.activity_weight <= 0:
            return

        allowed_at = self.last_activity + timedelta(
            seconds=self.activity_weight)

        if now >= allowed_at:
            return

        return allowed_at
