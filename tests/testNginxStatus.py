import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../sources/server/')
import unittest

from modules.NginxStatus import NginxStatus


class TestNginxStatus(unittest.TestCase):
    """NginxStatus Unit Tests"""

    def test_init(self):
        """Instatiation"""
        nginx_status = NginxStatus()

    def test_get(self):
        """Data getter"""
        nginx_status = NginxStatus()
        self.assertEqual({}, nginx_status.get())

    def test_poll_metrics(self):
        """Poll Metrics"""
        nginx_status = NginxStatus()
        self.assertEqual({}, nginx_status.poll_metrics({}))

    def test_collect_metrics(self):
        """Collect Metrics"""
        nginx_status = NginxStatus()
        nginx_status.collect_metrics({})
        self.assertEqual({}, nginx_status.get())


if __name__ == '__main__':
    unittest.main()
