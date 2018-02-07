# pyTrivialCache

[![PyPI](https://img.shields.io/pypi/v/pyTrivialCache.svg)](https://pypi.python.org/pypi/pyTrivialCache)

The poor man's API for manipulating a file system cache.

### Usage

As a standalone script:

        $ cd /tmp
        $ touch a b c

        $ pyTrivialCache --basedir $(mktemp -d)
        Welcome to the pyTrivialCache shell.  Type help or ? to list commands.

        (pyTrivialCache:ZILAYMHG) list

        (pyTrivialCache:ZILAYMHG) push a
        Pushing a unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) push b
        Pushing b unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) push c
        Pushing c unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list
        a
        b
        c

        (pyTrivialCache:ZILAYMHG) unpush c
        Unpushing c from ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list
        a
        b

        (pyTrivialCache:ZILAYMHG) purge
        Unpushing a from ZILAYMHG.
        Unpushing b from ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list

        (pyTrivialCache:ZILAYMHG) quit
        Disconnected from ZILAYMHG.
