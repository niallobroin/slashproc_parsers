#!/usr/bin/env python
import json
import urllib2
import unittest
import threading

from slashproc_parser.basic_server import SimpleThreadedJSONRPCServer, SERVER_PORT
from slashproc_parser.basic_server import get_parsers, get_groups, get_vars, get_data


class TestBasicServer(unittest.TestCase):
    
    def setUp(self):
        address = ('localhost', SERVER_PORT)
        self.server = SimpleThreadedJSONRPCServer(address)
        self.server.register_function(get_parsers)
        self.server.register_function(get_groups)
        self.server.register_function(get_vars)
        self.server.register_function(get_data)
        self.server_url = "http://{}:{}".format(*address)
        threading.Thread(target=self.serve).start()

    def tearDown(self):
        self.server.shutdown()

    def serve(self):
        try:
            self.server.serve_forever()
        finally:
            self.server.server_close()

    def test_get_requests(self):
        get_requests = (
            '/slashproc/meminfo/memfree',
            '/slashproc/cpuinfo/model_name',
            '/slashproc/cpuinfo/bogomips/core_id',
            '/slashproc/uptime')

        for request in get_requests:
            r = urllib2.urlopen(self.server_url + request)
            result = json.loads(r.read().decode('ascii'))["result"]
            self.assertTrue("found" in result, "parameter should be found but was not")


if __name__ == '__main__':
    unittest.main()
