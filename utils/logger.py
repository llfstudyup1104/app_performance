import logging
import platform
import logging.handlers

def init_delog():
    logging.getLogger('paramiko').setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    
    logger.addHandler(console)

    return logger

# Add new function to log data into syslog on linux
def log_to_syslog(data, logger_name='logger_name', syslog_address='/dev/log', facility=16):
    if platform.system() != 'Linux':
        logging.info("log_to_syslog() is only supported on Linux")
        return
    
    logger_metrics = logging.getLogger(name=logger_name)
    formatter_syslog = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_metrics.setLevel(logging.INFO)

    has_sysloghandler = False
    for h in logger_metrics.handlers():
        if isinstance(h, logging.handlers.SysLogHandler):
            has_sysloghandler = True
            break
    
    if not has_sysloghandler:
        handler_syslog = logging.handlers.SysLogHandler(syslog_address, facility=facility)
        handler_syslog.setFormatter(formatter_syslog)
        logger_metrics.addHandler(handler_syslog)
    
    logger_metrics.info("data: " + str(data))