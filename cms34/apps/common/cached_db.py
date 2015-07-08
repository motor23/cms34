# -*- coding:utf8 -*-
#
#
#  Usage: 
#  cdb = CachedDB(db, cache)
#  cquery = cdb.query(Model).filter_by(parent=5, type='text').order_by('id')
#  result = cquery.all()
#

class CachedQuery(object):

    def __init__(self, parent, cls, items=None, with_polymorphic=False):
        self.parent = parent
        self.with_polymorphic = with_polymorphic
        self.cls = cls
        if items is None:
            self.items = parent.items(cls, with_polymorphic=with_polymorphic)
        else:
            self.items = items

    def filter_by(self, **kwargs):
        result = []
        for item in self.items:
            for key, value in kwargs.items():
                if getattr(item, key)!=value:
                    break
            else:
                result.append(item)
        return self.__class__(self.parent, self.cls, result)

    def __iter__(self):
        return self.items.__iter__()

    def all(self):
        return self.items

    def first(self):
        return self.items and self.items[0] or None

    def count(self):
        return len(self.items)

    def order_by(self, field, direction='asc'):
        result = self.items
        result.sort(lambda x, y: cmp(getattr(x, field), getattr(y, field)))
        if direction=='desc':
            result.reverse()
        return self.__class__(self.parent, self.cls, result)


class CachedDb(object):

    def __init__(self, maker):
        self.maker = maker
        self.cached_query = {}
        self.db_maker = self.maker.db_maker
        self.cache = self.maker.cache
        self.clear()

    def query(self, cls, with_polymorphic=False):
        query = self.cached_query.get(cls.__name__)
        if query:
            return query
        else:
            query = self.maker.query_cls(self, cls,
                                         with_polymorphic=with_polymorphic)
            return self.cached_query.setdefault(cls.__name__, query)

    def items(self, cls, with_polymorphic=False):
        items = self.items_from_cache(cls)
        if items is None:
            items = self.items_from_db(cls, with_polymorphic=with_polymorphic)
            self.items_to_cache(cls, items)
        return items

    def items_key(self, cls):
        return self.maker.cache_prefix + cls.__name__

    def items_from_db(self, cls, with_polymorphic=False):
        db = self.maker.db_maker() #XXX
        query = db.query(cls)
        if with_polymorphic:
            query = query.with_polymorphic('*')
        result = query.limit(self.maker.db_limit).all()
        db.close()
        return result

    def items_from_cache(self, cls):
        if self.maker.cache_enabled:
            return self.cache.get(self.items_key(cls))

    def items_to_cache(self, cls, items):
        if self.maker.cache_enabled:
            self.cache.set(self.items_key(cls), items,
                           time=self.maker.cache_timeout)

    def clear(self):
        self.cached_query = {}


class CachedDbMaker(object):
    db_limit = 100
    cache_prefix = 'cached-db-'
    cache_enabled = True
    cache_timeout = 60
    query_cls = CachedQuery
    cached_db_cls = CachedDb

    def __init__(self, db_maker, cache, **kwargs):
        self.db_maker = db_maker
        self.cache = cache
        self.__dict__.update(kwargs)

    def __call__(self):
        return self.cached_db_cls(self)

