import os
from unittest import TestCase

from pyTrivialCache import pyTrivialCache

class Test(TestCase):
    def test(self):
        basedir = os.environ['PYTRIVIALCACHE_BASEDIR']
        wd = os.environ['PYTRIVIALCACHE_WD']

        os.chdir(wd)
        cache = pyTrivialCache(basedir)

        cache.push('a')
        cache.push('b')
        cache.push('c')

        self.assertTrue(len(cache.traverse()) == 3)

        cache.purge()

        self.assertTrue(len(cache.traverse()) == 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
