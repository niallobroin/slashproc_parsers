#!/usr/bin/env python

import re
from slashproc_parser.basic_parser import BasicSPParser


class CmdLine(BasicSPParser):
    """ Provides static methods for parsing /proc/cmdline file

        Attributes: CMDLINE (str): path to parsed file
    """

    CMDLINE = "/proc/cmdline"

    def __init__(self):
        super(CmdLine, self).__init__(self)

    @staticmethod
    def get_groups():
        """ Used for getting groups into which file is divided

            Returns: dict: groups
        """
        return {'cmdline': {'label': 'cmdline', 'parents': ['root']}}

    @staticmethod
    def get_vars():
        """ Used for getting variables descriptions from /proc/cmdline

            Each variable is represented by dictionary that contains variable name,
            list of groups that contain this variable and unit of measurement.

            Returns:
                thevars (dict): variables
        """

        descs = {
            'raw': {
                'desc': "The full kernel boot command",
                'label': "Command Kernel Line",
                'parents': ['cmdline']
            },

            'boot_image': {
                'desc': '',
                'label': "Boot Image",
                'parents': ['cmdline']
            },

            'ro': {
                'desc': "Mount root device read-only on boot",
                'label': "Kernel Permissions",
                'parents': ['cmdline']
            },

            'root': {
                'desc': "Location of the root filesystem image",
                'label': 'Root directory',
                'parents': ['cmdline']
            },

            'rhgb': {
                'desc': "Red Hat Graphical Boot. Graphical booting is supported",
                'label': 'Graphical Boot',
                'parents': ['cmdline']
            },

            'quiet': {
                'desc': "All verbose kernel messages except extremely serious should be suppressed at boot time",
                'label': 'Suppress boot messages',
                'parents': ['cmdline']
            },

            'lang': {
                'desc': "Language",
                'label': 'Language',
                'parents': ['cmdline']
            },
        }

        thevars = dict()
        data = CmdLine.get_data()

        # remove not appeared in cmd arguments
        for var in descs.keys():
            if var in data.keys():
                thevars[var] = dict()
                thevars[var]['desc'] = descs[var]['desc']
                thevars[var]['label'] = descs[var]['label']
                thevars[var]['parents'] = ['cmdline']

        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/cmdline. All variables are stored in single group.

            Returns: data (dict): dictionary with variables and their values
        """
        retdict = dict()

        with open(CmdLine.CMDLINE) as f:
            line = f.readline().strip('\n')
            retdict['raw'] = line

            for arg in line.split():

                if re.match('[\w_.]+=', arg):
                    pos = arg.find('=')
                    k, v = arg[:pos], arg[pos+1:]
                    retdict[CmdLine.key_format(k)] = v

                else:
                    retdict[CmdLine.key_format(arg)] = arg

        return retdict

if __name__ == "__main__":
    cl = CmdLine()
    cl.test_parse()
