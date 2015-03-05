# -*- coding: utf-8 -*-
from iktomi.unstable.db.sqla.factories import LangModelProxy
from iktomi.cms.menu import (Menu, MenuGroup, DashRow,
                             DashCol, DashI18nStream, DashStream)


def top_menu(env):
    return Menu(None, items=[
        Menu(u'Начало', endpoint='index'),
    ], env=env)


def dashboard(env):
    return MenuGroup([
        DashRow([
            DashCol(u'Администрирование', items=[
                DashStream('admins'),
            ]),
        ]),
    ], env=env)

