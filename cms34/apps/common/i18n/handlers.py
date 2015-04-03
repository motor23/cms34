# -*- coding: utf8 -*-
from iktomi.web import WebHandler, namespace
from iktomi.web.reverse import Location
from .lang import Lang


class LanguageLocation(Location):
    def __init__(self, *builders, **kwargs):
        self.langs = kwargs.pop('langs')
        Location.__init__(self, *builders, **kwargs)


class Language(WebHandler):
    def __init__(self, available, active):
        self.available = available
        self.active = active
        self._next_handler = namespace(active)

    def __call__(self, env, data):
        env.langs = [Lang(lang, env.root, env.cfg.I18N_TRANSLATIONS_DIR, 'front', 'iktomi-forms')
                     for lang in self.available]
        env.available_languages = self.available
        for lang in env.langs:
            if lang == self.active:
                lang.configure_environment(env)
            else:
                env.other_lang = lang
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
