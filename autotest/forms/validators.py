# -*- coding: utf-8 -*-
from flask.ext.wtf import regexp

from flask.ext.babel import lazy_gettext as _

NAME_RE = r'^[\w.+-_]+$'
is_legal_name = regexp(NAME_RE,
                       message=_("Please use words, numbers or caches,"
                                 "thanks!"))
TASKNAME_RE = r'^[\w_]+$'
is_legal_taskname = regexp(TASKNAME_RE,
                       message=_("Please use words, numbers or _,"
                                 "thanks!"))

SVN_RE = r'^\(.*[\);]$|\s*'
is_legal_svn = regexp(SVN_RE,
                       message=_("Please add like:('svn1','./');('svn2','./')"))
