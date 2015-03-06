#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser

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

            Returns: thevars (dict): variables
        """
        thevars = {
            'raw': {'desc': "The full kernel boot command",
                    'label': "Command Kernel Line",
                    'parents': ['cmdline'],},

            'boot_image':{'desc': '',
                        'label': "Boot Image",
                        'parents': ['cmdline'],},

            'ro': {'desc': "Permissions on the kernel",
                            'label': "Kernel Permissions",
                            'parents': ['cmdline'],},

            'root': {'desc': "Location of the root filesystem image",
                    'label': 'Root directory',
                    'parents': ['cmdline'],},
            
            'rhgb': {'desc': "Red Hat Graphical Boot. Graphical booting is supported",
                    'label': 'Graphical Boot',
                    'parents': ['cmdline'],},
            
            'quiet': {'desc': "All verbose kernel messages except extremely serious should be suppressed at boot time",
                    'label': 'Suppress boot messages',
                    'parents': ['cmdline'],},
                
            'lang': {'desc': "Language",
                    'label': 'Language',
                    'parents': ['cmdline'],},
                }
        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/cmdline. All variables are stored in single group.

            Returns: data (dict): dictionary with variables and their values
        """
        with open(CmdLine.CMDLINE) as l:
            raw = l.read()
            line = raw.split()
            for word in line:
                p = word.split('=')
                b = p[0]
                if len(p) == 2:
                    a = p[1]
                else:
                    a = p[0]
            data[b] = a
		
        return {'cmdline': data}

if __name__ == "__main__":
    cl = CmdLine()
    cl.test_parse()
