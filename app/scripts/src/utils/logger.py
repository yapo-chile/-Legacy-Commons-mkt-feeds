import logging

class logger(object):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)-2s [%(message)s]'
                            , level=logging.INFO)
        self.logger = logging.getLogger('loggingScript')
        
    def getLogInfo(self, message):
        return self.logger.info('%s' % message)

    def getLogError(self, message):
        return self.logger.error('%s' % message)

    def getLogWarn(self, message):
        return self.logger.warn('%s' % message)

    def getLogDebug(self, message):
        return self.logger.debug('%s' % message)