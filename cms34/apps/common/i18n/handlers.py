# -*- coding: utf8 -*-
from iktomi.web import WebHandler, namespace
from iktomi.web.reverse import Location
from .lang import Lang


class LanguageLocation(Location):
    def __init__(self, *builders, **kwargs):
        self.langs = kwargs.pop('langs')
        Location.__init__(self, *builders, **kwargs)


class H_SetActiveLanguage(WebHandler):
    def __init__(self, i18n, active):
        self.i18n = i18n
        self.active = active

    def __call__(self, env, data):
        self.i18n.set_active_lang(env, self.active)
        return self.next_handler(env, data)

    def _filter_locations(self, _locations):
        # recursively filter out LangLocation-s without
        # selected language
        return dict([(nm, (loc, self._filter_locations(scope)))
                     for (nm, (loc, scope)) in _locations.items()
                     if not isinstance(loc, LanguageLocation)
                     or self.active in loc.langs])

    def _locations(self):
        locations = WebHandler._locations(self)
        return self._filter_locations(locations)


def H_Language(i18n, active):
    return namespace(active) | H_SetActiveLanguage(i18n, active)


class for_languages(WebHandler):
    def __init__(self, *langs):
        self.langs = frozenset(langs)

    def __call__(self, env, data):
        env.available_languages = self.langs
        if env.lang in self.langs:
            return self.next_handler(env, data)

    def _locations(self):
        # XXX hack (may be simply set loc.langs = self.langs,
        #           not change a class?? But it is also a hack..)
        # iterate over nested locations and change their class
        # to LangLocation, which store all appropriate languages
        locations = WebHandler._locations(self)
        new_locations = {}
        for name, (loc, scope) in locations.items():
            cls = loc.__class__
            assert cls in [Location], \
                'for_languages sublocations class should be exact Location ' \
                'otherwise we can not be shure that location class change ' \
                'brakes nothing %s' % loc.__class__.__name__
            loc = LanguageLocation(*loc.builders, langs=self.langs)
            new_locations[name] = (loc, scope)
        return new_locations
