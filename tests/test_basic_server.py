#!/usr/bin/env python
import json
import pprint
import urllib2
import unittest
import threading

from slashproc_parser.basic_server import SimpleThreadedJSONRPCServer, SERVER_PORT
from slashproc_parser.basic_server import get_parsers, get_groups, get_vars, get_data


VERBOSE = False


class TestBasicServer(unittest.TestCase):
    
    def setUp(self):
        address = ('localhost', SERVER_PORT)
        self.root = 'slashproc'
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

    def assertRequests(self, requests):
        for request in requests:
            r = urllib2.urlopen('/'.join([self.server_url, self.root, request]))
            result = json.loads(r.read().decode('ascii'))['result']
            self.assertTrue(
                'found' in result,
                "parameter '%s' should be found but was not" % request)

            if VERBOSE:
                pprint.pprint(result)

    def test_simple_GET_requests(self):
        get_requests = (
            'uptime',
            'sysnet',
            'version',
            'meminfo/memfree',
            'cpuinfo/model_name',
            'cpuinfo/bogomips/core_id')

        self.assertRequests(get_requests)

    def test_groups_and_vars_GET_requests(self):
        get_requests = (
            'uptime/groups/',
            'uptime/vars/total',
            'vmstat/groups/',
            'syskernel/vars/core_pattern',
            'version/groups/',
            'version/vars/user')

        self.assertRequests(get_requests)

    def test_get_parsers_POST_request(self):
        data = json.dumps({"method": "get_parsers", "id": "1"})
        r = urllib2.Request(self.server_url, data)
        response = urllib2.urlopen(r)
        result = json.loads(response.read())

        for parser in get_parsers():
            self.assertIn(parser, result["result"], "Parser name '%s' not found" % parser)

    def test_simple_POST_requests(self):
        url = self.server_url

        post_requests = (
            {"method": "get_groups", "id": "2", "params": {"path": "/proc/uptime"}},
            {"method": "get_vars", "id": "3", "params": {"path": "/proc/uptime"}},
            {"method": "get_data", "id": "4", "params": {"path": "/proc/uptime/total"}},
            {"method": "get_data", "id": "5", "params": {"parser": "uptime", "get": "total"}}
        )

        for params in post_requests:
            data = json.dumps(params).encode()
            r = urllib2.Request(url, data)
            response = urllib2.urlopen(r)
            result = json.loads(response.read())
            self.assertIn("jsonrpc", result)
            self.assertIn("result", result)
            self.assertNotIn("err", result["result"], "Got unexpected error in request: %s" % params)

            if VERBOSE:
                pprint.pprint(result)


if __name__ == '__main__':
    unittest.main()
