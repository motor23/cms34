"""
http://jinja.pocoo.org/docs/extensions/
http://werkzeug.pocoo.org/docs/contrib/cache/
"""

from jinja2 import nodes
from jinja2.ext import Extension


class BlockCacheExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['cache'])

    cache_key_prefix = 'jinja2_cached_block_'

    def __init__(self, environment):
        super(BlockCacheExtension, self).__init__(environment)

        # add the defaults to the environment
        environment.extend(
            fragment_cache_prefix='',
            fragment_cache=None
        )

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        lineno = parser.stream.next().lineno

        # now we parse a single expression that is used as cache key.
        args = [parser.parse_expression()]

        # if there is a comma, the user provided a timeout.  If not use
        # None as second parameter.
        if parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(['name:endcache'], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(self.call_method('_cache_support', args),
            [], [], body).set_lineno(lineno)

    def _cache_support(self, name, timeout=None, caller=None):
        """Helper callback."""
        #enabled = getattr(self.environment.cfg, 'CACHE_PAGES_ENABLED', True)
        env = self.environment.globals['env']

        enabled = env.cfg.CACHE_BLOCKS_ONLY or env.cfg.CACHE_ENABLED
        if not enabled:
            return caller()

        if not timeout:
            timeout = getattr(env.cfg, 'CACHE_BLOCKS_TIME', 60)

        key = '_'.join([self.cache_key_prefix, name, env.lang])

        # try to load the block from the cache
        # if there is no fragment in the cache, render it and store
        # it in the cache.
        rv = env.cache.get(key)
        if rv is not None:
            return rv
        rv = caller()
        env.cache.set(key, rv, timeout)
        return rv
