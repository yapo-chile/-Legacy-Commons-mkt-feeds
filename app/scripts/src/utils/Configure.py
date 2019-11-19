import sys
import logging

class Conf(object):
    # Construtor
    def __init__(self, conf_file ):
        self.logger =  logging.getLogger('conf')
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d - %(funcName)20s()] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)
        self.conf_file = conf_file
        self.conf = {}
        self.load_conf()

    def get_specific(self, key):
        return self.conf.get(key)

    def get_all(self):
        return self.conf

    def get_logger( self ):
        return self.logger

    def load_conf(self):
        try:
            self.logger.info('Load configuration. Read file %s .' % self.conf_file )
            with open(self.conf_file, 'r') as f:
                for line in f.readlines():
                    if line.strip() and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        self.conf[k] = v
                        self.logger.info('%s : %s' % ( k , v ) )
        except Exception as e:
            self.logger.error('%s' % e )
            sys.exit()
