#!/usr/bin/env python

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
        retdict = Version.get_data()
        thevars = dict()
        for i in retdict.keys():
            thevars[Version.key_format(i)] = {
                'label': i,
                'unit': '',
                'parents': ['version']
            }

        descs = {
            ('ker_ver', 'Exact version of the Linux kernel used in the OS.', ''),
            ('user', 'Name of the user who compiled the kernel, and also a host name where it happened.', '')
            ('gcc_ver', 'Version of the GCC compiler used for building the kernel.', '')
            ('redhat_ver', 'RedHat version.', '')
            ('ker_type', 'Type of the kernel. SMP indicates Symmetric MultiProcessing.', '')
            ('ker_date', 'Date and time when the kernel was built.', '')
        }

        for var, desc, unit in descs:
            if var in thevars:
                thevars[var]['desc'] = desc
                thevars[var]['unit'] = unit
        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/version. All variables are stored in single group.

            Returns: stats (dict): dictionary with variables and their values
        """
        stats = dict()
        for l in open(Version.VERSION):
            line = l.split('(')
            version_data = {"ker_ver" : line[0].strip().replace('Linux version ', ''),
                            "user" : line[1].strip().replace(')', ''),
                            "gcc_ver" : line[2].strip().replace('gcc version ', ''),
                            "redhat_ver" : line[3].split('))')[0],
                            "ker_type" : " ".join(line[3].split('))')[1].split(' ')[1:3]),
                            "ker_date" : " ".join(line[3].split('))')[1].split(' ')[3:len(line[3])])}
        return {'version': version_data}

if __name__ == "__main__":
    ut = Version()
    ut.test_parse()