#!/usr/bin/env python

import unittest

from sp_parser.sp_server import *


class TestSPParser_input_validation(unittest.TestCase):

    def setUp(self):

        res = ['core0', 'core1', 'coreid']

        self.test_data = [
            (u'/proc/cpuinfo', '', '', []),
            (u'/proc/cpuinfo/core0', '', '', ['core0']),
            (u'/proc/cpuinfo/core0/coreid', '', '', ['core0', 'coreid']),

            (u'', u'/proc/cpuinfo', '', []),
            (u'', u'/proc/cpuinfo/core0', '', ['core0']),
            (u'', u'/proc/cpuinfo/core0/coreid', '', ['core0', 'coreid']),

            (u'', u'cpuinfo', u'core0', ['core0']),
            (u'', u'cpuinfo', u'core0, core1', ['core0', 'core1']),
            (u'', u'cpuinfo', u'core0, coreid', ['core0', 'coreid']),

            #Mixed use, but should still parse, path takes priority
            (u'/cpuinfo/core0/', u'cpuinfo', "core0, coreid", ['core0']),
            (u'', u'cpuinfo', u'core0, core1, coreid', res),
            (u'cpuinfo', u'cpuinfo', u'core0, core1, coreid', []),

            #Allowed separator
            (u'', u'cpuinfo', u'core0, core1, coreid', res),
            (u'', u'cpuinfo', u'core0. core1, coreid', res),
            (u'', u'cpuinfo', u'core0| core1, coreid', res),
            (u'', u'cpuinfo', u'core0/core1, coreid', res),

            #Lists can be passed into the function through json
            ([u'/cpuinfo/core0/'], u'cpuinfo', "core0, coreid", ['core0']),
            (u'', [u'cpuinfo'], u'core0, core1, coreid', res),
            (u'cpuinfo', u'cpuinfo', [u'core0, core1, coreid'], []),
            ]

    def test_input_validation(self): 
        for t in self.test_data:
            parser, get = input_validation(t[0], t[1], t[2])

            self.assertEquals(parser, u'cpuinfo')
            self.assertEqual(get, t[3])



