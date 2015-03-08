#!/usr/bin/env python

import re
from sp_parser.basic_sp_parser import BasicSPParser


class Version(BasicSPParser):
    """ Provides static methods for parsing /proc/version file

        Attributes: VERSION (str): path to parsed file
    """

    VERSION = "/proc/version"

    def __init__(self):
        super(Version, self).__init__(self)

    @staticmethod
    def get_groups():
        """ Used for getting groups into which file is divided

            Returns: dict: groups
        """
        return {'version': {'label': 'version', 'parents': ['root']}}

    @staticmethod
    def get_vars():
        """ Used for getting variables descriptions from /proc/version

            Each variable is represented by dictionary that contains variable name,
            list of groups that contain this variable and unit of measurement.

            Returns: thevars (dict): variables
        """
        thevars = {
            'ker_ver': {
                'desc': "Exact version of the Linux kernel used in the OS",
                'label': 'Kernel Version',
                'unit': '',
                'parents': ['version']
            },
            'user': {
                'desc': "User who compiled the kernel, host name where it happened",
                'label': 'Username, hostname',
                'unit': '',
                'parents': ['version']
            },
            'gcc_ver': {
                'desc': "Version of the GCC compiler used for building the kernel",
                'label': 'GCC Version',
                'unit': '',
                'parents': ['version']
            },
            'os_ver': {
                'desc': "OS version",
                'label': 'OS Version',
                'unit': '',
                'parents': ['version']
            },
            'ker_type': {
                'desc': "Type of the kernel. SMP indicates Symmetric MultiProcessing",
                'label': 'Kernel Type',
                'unit': '',
                'parents': ['version']
            },
            'ker_date': {
                'desc': "Date and time when the kernel was built",
                'label': 'Date of compilation',
                'unit': '',
                'parents': ['version']
            }
        }
        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/version. All variables are stored in single group.

            Returns:
                data (dict): dictionary with variables and their values
        """
        retdict = dict()

        kernel_regex = [
            ('ker_ver', '[-.\d]+\w+'),
            ('user', '\(\w+@\w+\)'),
            ('gcc_ver', '\(gcc version [.\d]+\s+.*\)'),
        ]

        with open(Version.VERSION) as l:
            line = l.readline().strip('\n')

            kernel_ver, os_ver = line.split('#')

            for var, pattern in kernel_regex:
                m = re.search(pattern, kernel_ver)
                retdict[var] = kernel_ver[m.start(): m.end()]

            m = re.search('(Mon|Tue|Wed|Thu|Fri|Sat|Sun)', os_ver)

            ker_date = os_ver[m.start():]
            os_ver, ker_type = os_ver.replace(ker_date, '').strip().split()

            retdict['ker_date'] = ker_date
            retdict['os_ver'] = os_ver
            retdict['ker_type'] = ker_type

        # leave only innermost braces
        return {k: v.strip('()').strip(' ')
                for k, v in retdict.iteritems()}


if __name__ == "__main__":
    ut = Version()
    ut.test_parse()
