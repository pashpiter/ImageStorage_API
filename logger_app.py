import logging


_log_format = '%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: '\
              '%(levelname)s: %(message)s'


class CustomFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> None:
        """Добавление произвольного поля в вывод логов"""
        record.route = record.args.get('route', None) if record.args else None
        record.functionName = record.funcName
        return True


def set_level_and_formatter(
        handler: tuple[logging.FileHandler, logging.StreamHandler]
) -> None:
    """Установка уровня уведомлений и форматтера для обработчика"""
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(_log_format, "%Y-%m-%d %H:%M:%S"))


def get_filehandler() -> logging.FileHandler:
    """Настройка файлового обработчика для логов"""
    handler = logging.FileHandler('logs.log', mode='a', encoding='UTF-8')
    set_level_and_formatter(handler)
    return handler


def get_streamhandler() -> logging.StreamHandler:
    """Настройка консольного обработчика для логов"""
    handler = logging.StreamHandler()
    set_level_and_formatter(handler)
    return handler


def get_logger(name: str) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_filehandler())
    logger.addHandler(get_streamhandler())
    logger.addFilter(CustomFilter())
    return logger
