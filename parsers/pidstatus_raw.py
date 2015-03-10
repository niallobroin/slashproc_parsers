#!/usr/bin/env python

import re
import os
import glob
from itertools import chain
from collections import defaultdict
from sp_parser.basic_sp_parser import BasicSPParser


class PidStatusRaw(BasicSPParser):
    """
    Provides static methods for parsing /proc/[0-9]*/status files

    Attributes:
        PID_RAW (str): regex that used to iterate over all status files
    """

    PID_RAW = "/proc/[0-9]*/status"

    def __init__(self):
        super(PidStatusRaw, self).__init__(self)

    @staticmethod
    def get_groups():
        """Enumerate groups depending on number of processes in current session

        Returns:
            retdict (dict): parsed groups
        """

        retdict = PidStatusRaw.parse_pidstatus(mode='relations_only')
        groups = {'pidstatus_raw': {
                  'label': 'PID statuses of all processes in session',
                  'parents': ['root']}}

        parents = dict()

        def traverse(pid, subdict):
            if 'parents' not in subdict:
                parents[pid] = ['pid']
            else:
                parents[pid] = subdict['parents']
                del subdict['parents']

            for child in subdict.keys():
                traverse(child, subdict[child])

        # collects parent-child relations into plain dict
        traverse('0', retdict['pid']['0'])

        for pid in parents.keys():
            groups[PidStatusRaw.key_format(pid)] = {
                'label': pid,
                'parents': parents[pid]
            }

        return groups

    @staticmethod
    def get_vars():
        """Create variables from all collected processes.

        Each process status can has variables that were not already met
        so need iterate over all processes to collect all available keys.

        Returns:
            thevars (dict): PID status variables
        """

        retdict = PidStatusRaw.parse_pidstatus(mode='flat')
        processes = retdict['pid'].keys()
        parents = defaultdict(set)

        for pid in processes:
            for i in retdict['pid'][pid].keys():
                parents[i].add(pid)

        thevars = dict()
        all_keys = set(chain.from_iterable(retdict['pid'][pid].keys() for pid in processes))

        for key in all_keys:
            thevars[PidStatusRaw.key_format(key)] = {
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
        """ Collect data from PID directories """
        return PidStatusRaw.parse_pidstatus()

    @staticmethod
    def parse_pidstatus(mode='all'):
        """Parse /proc/[pid]/status for each process

        Result is grouped into pstree-like format. So each group name is PID
        number and each subgroup name also PID number that is connected with
        outer number with parent-child relation.

        Arguments:
            mode (str): how status should be processed

                all - collects all available PID statuses and relations
                    between processes
                flat - same as 'all' but without relations between PIDs
                relations_only - collects only PIDs relations
        """

        if mode not in ('flat', 'relations_only', 'all'):
            raise ValueError('incorrect processing mode')

        tabs = re.compile('\s+')
        processes_plain = {'pid': dict()}
        processes_relations = defaultdict(list)

        for status in glob.iglob(PidStatusRaw.PID_RAW):
            pid = status.split(os.sep)[2]

            entries = dict()

            for line in open(status):
                parts = [p.strip().replace(':', '') for p in tabs.split(line) if p and p != 'kB']
                k, v = parts[0], ' '.join(parts[1:])
                entries[PidStatusRaw.key_format(k)] = v

            processes_plain['pid'][pid] = entries
            processes_relations[entries['ppid']].append(pid)

        if mode == 'flat':
            return processes_plain

        # used to create hierarchical groups
        def traverse(root, subtree):
            current_layer = dict()
            for child in processes_relations[root]:
                traverse(child, current_layer)
            if mode == 'all':
                current_layer.update(processes_plain['pid'][root])
            current_layer['parents'] = [processes_plain['pid'][root]['ppid']]
            subtree[root] = current_layer

        tree, layer = {'pid': dict()}, dict()
        for c in processes_relations['0']:
            traverse(c, layer)

        tree['pid']['0'] = layer

        return tree


if __name__ == "__main__":
    ps = PidStatusRaw()
    ps.test_parse()