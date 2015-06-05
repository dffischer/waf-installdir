#! /usr/bin/env python

APPNAME = "waf-installdir"

from waflib.Context import waf_dir
from waflib.Utils import subst_vars

def configure(ctx):
    pass

def build(ctx):
    ctx.install_files(''.join((
        "${LIBDIR}/",
        waf_dir.rpartition('/')[2],
        "/waflib/extras")),
    'installdir.py')
