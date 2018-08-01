#!/usr/bin/env python
"""
    NginxStatus Class
"""
import logging
import logging.handlers
import socket
import urllib2


class NginxStatus:
    def __init__(self, url="http://127.0.0.1:8000/nginx_status"):
        logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
        self.logger = logging.getLogger('root')
        self.hostname = self._get_server_hostname()
        self._data = {}
        self.url = url
        self.collect_metrics()

    def get(self):
        return self._data

    def poll_metrics(self):
        self.collect_metrics()
        return self._data

    def collect_metrics(self):
        self._data = self._get_metrics()

    def _get_metrics(self):
        try:
            req = urllib2.Request(self.url)
            response = urllib2.urlopen(req)
            r1 = response.readline()        # Active connections: 4
            r2 = response.readline()        # server accepts handled requests
            r3 = response.readline()        # 1650 1650 9255
            r4 = response.readline()        # Reading: 0 Writing: 1 Waiting: 3'
            active = r1.split()[2]
            reading = r4.split()[1]
            writing = r4.split()[3]
            waiting = r4.split()[5]
            response.close()
            data = {'server': self.hostname,
                    'url': self.url,
                    'active': active,
                    'reading': reading,
                    'writing': writing,
                    'waiting': waiting}
            self.logger.debug('nginx_status:\n%s\n%s\n%s\n%s' % (r1, r2, r3, r4))
            return data
        except Exception, e:
            self.logger.error('Error retrieving nginx status: %s' % e)
            return {}

    def _get_server_hostname(self):
        try:
            hostname = socket.gethostname()
            return hostname
        except Exception, e:
            self.logger.error('Error reading hostname: %s' % e)
            return False

    def get_server_hostname(self):
        return self.hostname
