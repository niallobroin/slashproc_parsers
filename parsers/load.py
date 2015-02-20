#!/usr/bin/env python

import re
from sp_parser.basic_sp_parser import BasicSPParser


class Load(BasicSPParser):
    """
    The first three columns measure CPU and IO utilization of the last one, five, and 10 minute periods. The fourth column shows the number of currently running processes and the total number of processes. The last column displays the last process ID used.
    """

    PROC = "/proc/loadavg"

    def __init__(self):
        super(Load, self).__init__(self)

    @staticmethod
    def get_groups():
        """
        Static method to define vars that that parser can parse
        #Will probably be a class later.
        """
        GROUPS = {
            'loadavg': {'name': 'CPU', 'parents': ['root']}, 
                }
        return GROUPS
        
    @staticmethod
    def get_vars():
        """
        Static method to define vars that that parser can parse
        #Will probably be a class later.
        """
        parents = ['loadavg']
        thevars = {'loadavg_1min': {'name': "cpu and IO utilisation of the last 1 min",
                                    'parents': parents,
                                    'unit': '%'},
                   'loadavg_5mins': {'name': "cpu and IO utilisation of the last 5 mins",
                                       'parents': parents,
                                       'unit': '%'},
                   'loadavg_10mins': {'name': "cpu and IO utilisation of last 10 mins",
                                       'parents': parents,
                                       'unit': '%'},
                   'current_num_processes': {'name': "Current number of Processes",
                                       'parents': parents,
                                       'unit': '%'},
                   'total_num_processes': {'name': "Total number of processes",
                                       'parents': parents,
                                       'unit': '%'},
                   }
            
        return thevars


    def get_data(self):
        """

        """
        with open(Load.PROC, 'r') as f:
            a = f.read().split()

        return {'loadavg':{'loadavg_1min': a[0],
                           'loadavg_5mins': a[1],
                           'loadavg_10mins': a[2],
                           'curr_num_processes': a[3],
                           'total_num_processes': a[4],
               }}




if __name__ == "__main__":
    c = Load()
    c.test_parse()
