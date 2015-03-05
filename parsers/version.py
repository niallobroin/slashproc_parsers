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
        thevars = {
                'ker_ver': {'desc': "Exact version of the Linux kernel used in the OS",
                          'label': 'Kernel Version',
                          'unit': '',
                          'parents': ['version'],},

                'user': {'desc': "User who compiled the kernel, host name where it happened",
                         'label': 'Username, hostname',
                         'unit': '',
                         'parents': ['version'],},
				'gcc_ver': {'desc': "Version of the GCC compiler used for building the kernel",
                         'label': 'GCC Version',
                         'unit': '',
                         'parents': ['version'],},
				'redhat_ver': {'desc': "RedHat version",
                         'label': 'RedHat Version',
                         'unit': '',
                         'parents': ['version'],},
				'ker_type': {'desc': "Type of the kernel. SMP indicates Symmetric MultiProcessing",
                         'label': 'Kernel Type',
                        'unit': '',
                         'parents': ['version'],},
				'ker_date': {'desc': "Date and time when the kernel was built",
                         'label': 'Date of compilation',
                         'unit': '',
                         'parents': ['version'],},
                }
        return thevars

   @staticmethod
    def get_data():
        """ Parse /proc/version. All variables are stored in single group.

            Returns: data (dict): dictionary with variables and their values
        """
        with open(Version.VERSION) as l:
            raw = l.read()
        
		line = raw.split('(')
		
		for word in line:
			if "Linux version" in w:
				data['ker_ver'] = w.strip().replace('Linux version ', '')
			if "@" in w:
				data['user'] = w.strip().replace(')', '')
			if "gcc" in w:
				data['gcc_ver'] = w.strip().replace('gcc version ', '')
			if "Red Hat" in w:
				a = w.split(')')
				data['redhat_ver'] = a[0].replace('Red Hat ', '')
			if "#1" in w:
				a = w.split("#1")
				data['ker_date'] = a[1]
			
        return {'version': data}

if __name__ == "__main__":
    ut = Version()
    ut.test_parse()
