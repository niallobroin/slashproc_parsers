#!/usr/bin/env python

import re
import os
import glob
from sp_parser.basic_sp_parser import BasicSPParser


class PidParser(BasicSPParser):
    """
    Provides static methods for parsing highest processes from /proc/[PID]
    """

    PID = "/proc/[0-9]*/status"

    @staticmethod
    def get_groups():
        """
        """
        retdict = PidParser.get_data()

        groups = {'pidparser': {'label': 'pidparser', 'parents': ['root']}}

        for pid in retdict['pid'].keys():
            groups[PidParser.key_format(pid)] = {
                'label': pid,
                'parents': [retdict['pid'][pid]['ppid']]
            }

        return groups


    @staticmethod
    def get_vars():
        """
        """
        retdict = PidParser.get_data()
        thevars = dict()

        for pid in retdict['pid'].keys():
            thevars[pid] = {
                'label': pid,
                'unit': '',
                'parents': [retdict['pid'][pid]['ppid']]
            }

        return thevars


    @staticmethod
    def get_data():
        """Parse /proc/[pid]/status for highest processes (i.e. 0-pid children)
        """
        tabs = re.compile('\s+')

        pids = dict()

        for status in glob.iglob(PidParser.PID):
            pid = status.split(os.sep)[2]
            entries = dict()

            for line in open(status):
                parts = [p.strip().replace(':', '') for p in tabs.split(line) if p and p != 'kB']
                k, v = parts[0], ' '.join(parts[1:])
                entries[PidParser.key_format(k)] = v

            if entries['ppid'] == '0':
                pids[pid] = entries

        return {'pid': pids}


if __name__ == "__main__":
    pp = PidParser()
    pp.test_parse()