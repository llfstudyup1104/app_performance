import logging
import logging.handlers

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address='/tmp/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

log.debug('This is debug')