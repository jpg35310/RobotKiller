# -*-coding: utf8 -*
from __future__ import print_function, absolute_import, unicode_literals

import sys
import traceback
import logging
import coloredlogs
import time
from gettext import gettext as _

logger = logging.getLogger('emballage')
logger.setLevel(logging.DEBUG)

logging_format = "%(asctime)s %(levelname)s [%(module)s:%(funcName)s():%(lineno)d] %(message)s"
coloredlogs.install(level='DEBUG', logger=logger, fmt=logging_format)

LAST_MSG = ''


def print_exception(msg=None):
    global LAST_MSG
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = "".join(traceback.format_tb(exc_traceback))
    if msg and len(msg):
        msg = 'Message: %s ' % msg
    else:
        msg = ''

    if LAST_MSG != exc_value.message:
        LAST_MSG = exc_value.message
        logger.error(_("%sError: %s") % (msg, LAST_MSG))
        logger.debug(_("Type: %s") % exc_type)
        logger.debug(tb)