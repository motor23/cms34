# -*- coding: utf-8 -*-

from cms34.mixed.fields import XF_DateTime, XF_String, XF_Int


class XF_Ip(XF_String):
    name = 'ip'
    max_length = 16


class XF_LastActivity(XF_DateTime):
    name = 'last_activity'


class XF_ActivityWeight(XF_Int):
    name = 'activity_weight'
    initial = 0


class XF_ActivityType(XF_String):
    name = 'activity_type'
    max_length = 80


xf_ip = XF_Ip()
xf_last_activity = XF_LastActivity()
xf_activity_weight = XF_ActivityWeight()
xf_activity_type = XF_ActivityType()
