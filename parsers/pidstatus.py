#!/usr/bin/env python

import re
import os
import glob
from collections import defaultdict
from itertools import chain
from sp_parser.basic_sp_parser import BasicSPParser


class PidStatus(BasicSPParser):

    PID = "/proc/[0-9]*/status"

    def __init__(self):
        super(PidStatus, self).__init__(self)

    @staticmethod
    def get_groups():
        """Enumerate groups depending on number of processes in current session

        Returns:
            retdict (dict):
        """
        retdict = PidStatus.parse_pidstatus()
        groups = {'pid': {'name': 'pisstatus', 'parents': ['root']}}

        for i in retdict['pid']:
            groups[PidStatus.key_format(i)] = {'name': i, 'parents': ['pid']}

        return groups

    @staticmethod
    def get_vars():
        """ Create variables from all collected processes.

        Each process status can has variables that were not already met
        so need iterate over all processes to collect all available keys.

        Returns:
            thevars (dict):
        """

        retdict = PidStatus.parse_pidstatus()
        processes = retdict['pid'].keys()
        parents = defaultdict(set)

        for pid in processes:
            for i in retdict['pid'][pid].keys():
                parents[i].add(pid)

        thevars = dict()
        all_keys = set(chain.from_iterable(retdict['pid'][pid].keys() for pid in processes))

        for pid in processes:
            for key in all_keys:

                thevars[PidStatus.key_format(key)] = {
                    'name': key,
                    'unit': '',
                    'parents': list(parents[key])
                }

        # is not used yet
        descs = [
            ('Name', 'Command run by this process', ''),
            ('State', 'Current state of the process', ''),
            ('Tgid', 'Thread group ID (i.e., Process ID)', ''),
            ('Ngid', '', ''),
            ('Pid', 'Thread ID'),
            ('PPid', 'PID of parent process', ''),
            ('TracerPid', 'PID of process tracing this process (0 if not being traced)', ''),
            ('Uid', 'Real, effective, saved set, and filesystem UIDs', ''),
            ('Gid', 'Real, effective, saved set, and filesystem GIDs', ''),
            ('FDSize', 'Number of file descriptor slots currently allocated', ''),
            ('Groups', 'Supplementary group list', ''),
            ('VmPeak', 'Peak virtual memory size', 'kB'),
            ('VmSize', 'Virtual memory size', 'kB'),
            ('VmLck', 'Locked memory size', 'kB'),
            ('VmHWM', 'Peak resident set size ("high water mark")', 'kB'),
            ('VmRSS', 'Resident set size', 'kB'),
            ('VmData', 'Size of data segment', 'kB'),
            ('VmStk', 'Size of stack segment', 'kB'),
            ('VmExe', 'Size of text segment', 'kB'),
            ('VmLib', 'Shared library code size', 'kB'),
            ('VmPTE', 'Page table entries size (since Linux 2.6.10)', 'kB'),
            ('VmSwap', '', 'kB'),
            ('Threads', 'Number of threads in process containing this thread', ''),
            ('SigQ', 'This field contains two slash-separated numbers that '
                     'relate to queued signals for the real user ID of this '
                     'process.  The first of these is the number of currently '
                     'queued signals for this real user ID, and the second is the '
                     'resource limit on the number of queued signals for this process', ''),
            ('', '', ''),
            ('', '', ''),
            ('', '', ''),
        ]

        return thevars

    @staticmethod
    def get_data():
        return PidStatus.parse_pidstatus()

    @staticmethod
    def parse_pidstatus():
        """Parse /proc/[pid]/status for each process

        """
        retdict = {'pid': dict()}
        tabs = re.compile('\s+')

        for status in glob.iglob(PidStatus.PID):
            pid = status.split(os.sep)[2]

            entries = dict()

            for line in open(status):
                parts = [p.strip().replace(':', '') for p in tabs.split(line) if p and p != 'kB']
                k, v = parts[0], ' '.join(parts[1:])
                entries[PidStatus.key_format(k)] = v

            retdict['pid'][pid] = entries

        return retdict


if __name__ == "__main__":
    ps = PidStatus()
    ps.test_parse()