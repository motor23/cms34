# -*- coding:utf8 -*-
from .handlers import H_Language
from .lang import Lang

class I18n(object):

    available = ['ru', 'en']
    categories = ['front', 'iktomi-forms']
    translations_dir = None

    def __init__(self, available=[], translations_dir=None, categories=[]):
        self.categories = categories or self.categories
        self.available = available or self.available
        self.translations_dir = translations_dir or self.translations_dir

    def create_langs(self, env):
        return [Lang(lang, env.root, self.translations_dir, self.categories) \
                                                    for lang in self.available]

    def handler(self, active):
        return H_Language(self, active)

    def set_active_lang(self, env, active):
        env.langs = self.create_langs(env)
        assert active in env.langs
        env.available_languages = env.langs
        for lang in env.langs:
            if lang == active:
                env.lang = lang
                env._root = env.root
                env.root = lang.root
                env._namespace = env.namespace
                del env.namespace
            else:
                env.other_lang = lang

    def __iter__(self):
        return self.langs

