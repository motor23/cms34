# -*- coding:utf8 -*-
#
#
#  Usage: 
#  cdb = CachedDB(db, cache)
#  cquery = cdb.query(Model).filter_by(parent=5, type='text').order_by('id')
#  result = cquery.all()
#

from sqlalchemy.ext.serializer import dumps, loads


class NoSuchAttribute(object):
    """
    This should be used as safe default value for getattr.
    """
    pass


class CachedQuery(object):
    def __init__(self, items):
        self.items = items

    def filter_by(self, **kwargs):
        result = []
        for item in self.items:
            for key, value in kwargs.items():
                if getattr(item, key, NoSuchAttribute) != value:
                    break
            else:
                result.append(item)
        return self.__class__(result)

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
        if direction == 'desc':
            result.reverse()
        return self.__class__(result)

    def as_dict(self):
        return dict([(i.id, i) for i in self.items])


class CachedDb(object):
    def __init__(self, cache, cache_enabled=True, cache_prefix='cached-db-',
                 cache_timeout=60, query_cls=CachedQuery, bind_to_session=True):
        self.cache = cache
        self.cache_enabled = cache_enabled
        self.cache_prefix = cache_prefix
        self.cache_timeout = cache_timeout
        self.query_cls = query_cls
        self.queries = {}
        self.bind_to_session = bind_to_session

    def query(self, query_id, _query, reload=False):
        if not isinstance(query_id, basestring):
            query_id = query_id.__name__
        if not reload and self.queries.has_key(query_id):
            return self.queries[query_id]

        items = self.items_from_cache(query_id)
        if items is None:
            items = _query.all()
            self.items_to_cache(query_id, items)
        elif self.bind_to_session:
            items = map(lambda x: _query.session.merge(x, load=False), items)

        query = self.query_cls(items)
        self.queries[query_id] = query
        return query

    def items_key(self, query_id):
        return self.cache_prefix + query_id

    def items_from_cache(self, query_id):
        if self.cache_enabled:
            objs = self.cache.get(self.items_key(query_id))
            if objs is not None:
                return loads(objs)

    def items_to_cache(self, query_id, items):
        if self.cache_enabled:
            self.cache.set(self.items_key(query_id), dumps(items),
                           time=self.cache_timeout)

    def close(self):
        self.queries = {}
