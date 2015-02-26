#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser

class UpTime(BasicSPParser):
    """ Provides static methods for parsing /proc/uptime file

        Attributes: UPTIME (str): path to parsed file
    """

    UPTIME = "/proc/uptime"

    def __init__(self):
        super(UpTime, self).__init__(self)

    @staticmethod
    def get_groups():
        """ Used for getting groups into which file is divided

            Returns: dict: groups
        """
        return {'uptime': {'label': 'uptime', 'parents': ['root']}}

    @staticmethod
    def get_vars():
        """ Used for getting variables descriptions from /proc/uptime

            Each variable is represented by dictionary that contains variable name,
            list of groups that contain this variable and unit of measurement.

            Returns: thevars (dict): variables
        """
        thevars = {
                'total': {'desc': "The total number of seconds the system has been up",
                          'label': 'Total Uptime',
                          'unit': 'Seconds',
                          'parents': ['uptime'],},

                'idle': {'desc': "The total number of seconds the system has been up and idle",
                         'label': 'Idle Uptime',
                         'unit': 'Seconds',
                         'parents': ['uptime'],},
                }
        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/uptime. All variables are stored in single group.

            Returns: stats (dict): dictionary with variables and their values
        """
        stats = dict()
        for l in open(UpTime.UPTIME):
            line = l.split()

            uptime_data = {"total": line[0],
                           "idle":  line[1]}
        return {'uptime': uptime_data}

if __name__ == "__main__":
    ut = UpTime()
    ut.test_parse()
