# pyTrivialCache - The poor man's API for manipulating a file system cache

# The MIT License (MIT)
#
# Copyright (c) 2014-5 Roberto Reale <roberto.reale82@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Roberto Reale"
__version__ = "0.1.0"


from ConfigParser import ConfigParser
import os
import re
import logging
import logging.config


class pyTrivialCacheException(Exception):
    pass


class pyTrivialCacheLockException(pyTrivialCacheException):
    pass


class pyTrivialCacheConfig(ConfigParser):

    @property
    def name(self):
        return self._name

    @property
    def logger(self):
        return self.get(self._section, 'logger')

    @property
    def basedir(self):
        return self.get(self._section, 'basedir')

    @property
    def lock_dir(self):
        return os.path.join(self.basedir, '.lock_dir')

    @property
    def filter(self):
        return self.get(self._section, 'filter')

    @property
    def filter_pattern(self):
        return re.compile(self.filter)

    def __init__(self, config_file, trivial_cache_name='trivial_cache'):
        ConfigParser.__init__(self)
        self.read(config_file)
        self._name = trivial_cache_name
        self._section = trivial_cache_name

    def __del__(self):
        pass


class pyTrivialCache(pyTrivialCacheConfig):

    def lock(self):
        if not self.connected:
            try:
                os.makedirs(self.lock_dir)
                self.connected = True
                self.log(20, "Connected to %s." % self.name)
            except:
                self.log(30, "Cannot acquire lock on %s." % self.name)
                raise pyTrivialCacheLockException
        else:
                self.log(10, "Already connected to %s." % self.name)

    def unlock(self):
        if self.connected:
            try:
                os.rmdir(self.lock_dir)
                self.connected = False
                self.log(20, "Disconnected from %s." % self.name)
            except:
                self.log(30, "Cannot release lock on %s." % self.name)
                raise
        else:
            self.log(10, "Already disconnected from %s." % self.name)

    def _filename2path(self, filename):
        match = self.filter_pattern.match(filename)
        if match:
            intermediate = list(match.groups())
            return os.path.join(self.basedir, *intermediate)

    def _get_target_path(self, filename):
        return self._filename2path(filename)

    def get_full_path(self, filename):
        return os.path.join(self._get_target_path(filename), filename)

    def exists(self, filename, target_path=None):
        if not target_path:
            target_path = self._get_target_path(filename)
        full_target_path = os.path.join(target_path, filename)
        return os.path.exists(full_target_path)

    def push(self, filename, target_path=None):
        self.log(20, "Pushing %s unto %s." % (filename, self.name))
        if not target_path:
            target_path = self._get_target_path(filename)
        try:
            os.makedirs(target_path)
        except:
            pass
        return os.path.join(target_path, filename)

    def unpush(self, filename):
        self.log(20, "Unpushing %s from %s." % (filename, self.name))
        target_path = self._get_target_path(filename)
        full_target_path = os.path.join(target_path, filename)
        try:
            os.unlink(full_target_path)
        except:
            pass

    def traverse(self, sorter=None, full_path=False):
        all_files = []
        for dir_name, dirs, files in os.walk(self.basedir):
            for filename in files:
                if full_path:
                    all_files.append(os.path.join(dir_name, filename))
                else:
                    all_files.append(filename)
        if sorter:
            return sorted(all_files, key=sorter)
        else:
            return all_files

    def purge(self):
        for filename in self.traverse():
            self.unpush(filename)

    def __init__(self, config_file, trivial_cache_name='trivial_cache'):
        # set defaults
        self.connected = False
        # parse config file
        pyTrivialCacheConfig.__init__(self, config_file, trivial_cache_name)
        # initialize and start logging
        logging.config.fileConfig(config_file)
        self.logger_logger = logging.getLogger(self.logger)
        self.log = self.logger_logger.log

    def __del__(self):
        pass
