# pyTrivialCache - The poor man's API for manipulating a file system cache

# The MIT License (MIT)
#
# Copyright (c) 2014-7 Roberto Reale
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


import getopt
import sys



def short_usage():
    print >>sys.stderr, """Usage:
    pyTrivialCache -n NAME -b BASEDIR [ -p PATTERN ]
Try `pyTrivialCache --help' for more information."""


def full_usage():
    print >>sys.stderr, """Usage:
    pyTrivialCache -n NAME -b BASEDIR [ -p PATTERN ]
The poor man's API for manipulating a file system cache.
      --help                       display this help and exit
  -n, --name          NAME         name of the cache
  -b, --basedir       BASEDIR      base directory of the cache
  -p, --pattern       PATTERN      apply a patter match"""


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hn:b:p:",
                                   ["help", "name=", "basedir=", "pattern=", ])
    except getopt.GetoptError, err:
        print >>sys.stderr, err
        short_usage()
        sys.exit(2)

    name = None
    basedir = None
    pattern = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage()
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-n", "--basedir"):
            basedir = arg
        elif opt in ("-p", "--pattern"):
            pattern = arg

    # pre-flights sanity checks
    if not name:
        print >>sys.stderr, "Cache name not specified!\n"\
            "A used-defined name can be specified via the --name switch."
        sys.exit(2)
    if not basedir:
        print >>sys.stderr, "Cache basedir not specified!\n"\
            "A used-defined basedir can be specified via the --basedir switch."
        sys.exit(2)

    # connect to the cache shell
    pyTrivialCacheShell(name, basedir, pattern).cmdloop()


if __name__ == "__main__":
    main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
