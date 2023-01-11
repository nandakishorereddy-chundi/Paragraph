import logging

class Logger:
    '''
    Singleton Class which creates only one instance and returns the instance
    '''

    LOG_FMT = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s"

    __instance__ = None

    def __init__(self):
        if Logger.__instance__ is None:
            logr = logging.getLogger()
            fmtr = logging.Formatter(Logger.LOG_FMT)
            for h in logr.handlers: h.setFormatter(fmtr)
            logr.setLevel(logging.ERROR)
            Logger.__instance__ = self

    @staticmethod
    def get_instance():
        if Logger.__instance__ is not None:
            return Logger.__instance__

        Logger()
        return Logger.__instance__
    
    @staticmethod
    def log_info(message):
        logging.getLogger().info(message)

    @staticmethod
    def log_error(message):
        logging.getLogger().error(message)