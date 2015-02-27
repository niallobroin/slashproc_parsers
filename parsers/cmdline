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
        retdict = CmdLine.get_data()
        thevars = dict()
        for i in retdict.keys():
            thevars[CmdLine.key_format(i)] = {
                'label': i,
                'unit': '',
                'parents': ['cmdline']
            }

        descs = {
            ('ro', 'Indicates that the kernel is mounted read-only.', ''),
            ('root', 'Location of the root filesystem image.', ''),
            ('rhgb', 'Red Hat Graphical Boot. Indicates that graphical booting is supported', ''),
            ('quiet', '', 'Indicates that all verbose kernel messages except those which are extremely serious should be suppressed at boot time.'),
            ('spare', '', 'Spare')
        }

        for var, desc, unit in descs:
            if var in thevars:
                thevars[var]['desc'] = desc
                thevars[var]['unit'] = unit
        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/cmdline. All variables are stored in single group.

            Returns: stats (dict): dictionary with variables and their values
        """
        stats = dict()
        for l in open(CmdLine.CMDLINE):
            line = l.split()

            cmdline_data = {"ro": line[0],
                            "root":  line[1].strip().replace('root=', ''),
                            "rhgb":  line[2],
                            "quiet":  line[3],
                            "spare":  line[4]}
        return {'cmdline': cmdline_data}

if __name__ == "__main__":
    cl = CmdLine()
    cl.test_parse()