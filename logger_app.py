import logging

_log_format = f'%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: %(levelname)s: %(message)s'

class CustomFilter(logging.Filter):
     def filter(self, record):
        record.route = record.args.get('route', None) if record.args else None
        record.functionName = record.funcName
        return True

def get_handler():
    handler = logging.FileHandler('logs.log', mode='a', encoding='UTF-8')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(_log_format, ))
    return handler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_handler())
    logger.addFilter(CustomFilter())
    return logger
