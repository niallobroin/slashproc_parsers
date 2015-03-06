#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser
from parse_helpers import traverse_directory


class Dev(BasicSPParser):

    DEBUG = "/proc/sys/debug"

    @staticmethod
    def get_groups():
        """
        """
        _, parents, all_variables = traverse_directory(Debug.DEBUG)

        # no need to take into account variables
        for var in all_variables:
            del parents[var]

        groups = {'sysvm': {'label': 'Debug system variables', 'parents': ['root']}}

        for i in parents.keys():
            groups[Debug.key_format(i)] = {
                'label': i,
                'desc': '',
                'parents': parents[i]
            }

        return groups

    @staticmethod
    def get_vars():
        """
        """
        thevars = dict()
        _, parents, all_variables = traverse_directory(Debug.DEBUG)

        for var in all_variables:
            thevars[Debug.key_format(Debug)] = {
                'label': var,
                'unit': '',
                'parents': parents[var]
            }

        # TODO: fill with variables and appropriate descriptions
        descs = [

        ]

        return thevars

    @staticmethod
    def get_data(verbose=False):
        """
        """
        tree, _, _ = traverse_directory(Debug.DEBUG, verbose=verbose)
        return tree