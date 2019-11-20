from .logger import logger

class conf(object):
    def __init__(self, conf_file ):
        self.log = logger()
        self.conf_file = conf_file
        self.conf = {}
        self.loadConf()

    def getSpecific(self, key):
        return self.conf.get(key)

    def loadConf(self):
        try:
            self.log.getLogInfo('Load configuration. Read file ' + self.conf_file + '.' )
            with open(self.conf_file, 'r') as f:
                for line in f.readlines():
                    if line.strip() and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        self.conf[k] = v
                        self.log.getLogInfo('%s : %s' % ( k , v ) )
        except Exception as e:
            self.log.error('%s' % e )
