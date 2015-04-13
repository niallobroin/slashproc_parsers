#!/usr/bin/env python

import re
import os
import glob
from itertools import chain
from collections import defaultdict
from slashproc_parser.basic_parser import BasicSPParser


class PidStatus(BasicSPParser):

    PID = "/proc/[0-9]*/status"

    def __init__(self):
        super(PidStatus, self).__init__(self)

    @staticmethod
    def get_groups():
        """Enumerates groups depending on number of processes in current session.

        Each PID is converted into group and its status values - into variables.
        Children processes are treated as subgroups of their parent process group.

        Returns:
            retdict (dict): PID groups
        """

        # TODO: get_data was refactored, need to make changes here

        retdict = PidStatus.parse_pidstatus(mode='relations_only')
        groups = {'pid': {'label': 'pidstatus', 'parents': ['root']}}

        for i in retdict['pid']:
            groups[PidStatus.key_format(i)] = {'label': i, 'parents': ['pid']}

        return groups

    @staticmethod
    def get_vars():
        """Creates variables from all collected processes.

        Each process status can has variables that were not already met
        so need iterate over all processes to collect all available keys.

        Returns:
            thevars (dict):
        """

        retdict = PidStatus.parse_pidstatus(mode='flat')
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
                    'label': key,
                    'unit': '',
                    'parents': list(parents[key])
                }

        # TODO: fill missing description (and maybe variables too)
        descs = {
            'Name': {
                'desc': 'Command run by this process',
                'label': "Name of the Process",
                'parents': ['pidstatus']
            },

            'State': {
                'desc': 'Current state of the process. One of "R(running)", "S (sleeping)", "D (disk sleep)", "T (stopped)", "T (tracing stop)", "Z (zombie)", or "X (dead)"',
                'label': "State of the Process",
                'parents': ['pidstatus']
            },

            'Tgid': {
                'desc': 'Thread group ID (i.e., Process ID)',
                'label': "Thread Group ID",
                'parents': ['pidstatus']
            },

            'Pid': {
                'desc': 'Thread ID',
                'label': "Process ID",
                'parents': ['pidstatus']
            },

            'PPid': {
                'desc': 'PID of parent process',
                'label': "Parent Process ID",
                'parents': ['pidstatus']
            },

            'TracerPid': {
                'desc': 'PID of process tracing this process (0 if not being traced).',
                'label': "Tracing Process ID",
                'parents': ['pidstatus']
            },

            'Uid': {
                'desc': 'Real, effective, saved set, and file system UIDs',
                'label': "UID",
                'parents': ['pidstatus']
            },

            'Gid': {
                'desc': 'Real, effective, saved set, and file system GIDs',
                'label': "GID",
                'parents': ['pidstatus']
            },

            'FDSize': {
                'desc': 'Number of file descriptor slots currently allocated',
                'label': "File Descriptor Size",
                'parents': ['pidstatus']
            },

            'Groups': {
                'desc': 'Supplementary group list',
                'label': "Supplementary Groups",
                'parents': ['pidstatus']
            },

            'VmPeak': {
                'desc': 'Peak of the virtual memory size',
                'label': "Virtual Memory Peak",
                'parents': ['pidstatus']
            },

            'VmSize': {
                'desc': 'Size of the virtual memory',
                'label': "Virtual Memory Size",
                'parents': ['pidstatus']
            },

            'VmLck': {
                'desc': 'Size of the locked virtual memory',
                'label': "Virtual Memory Locked",
                'parents': ['pidstatus']
            },

            'VmHWM': {
                'desc': 'Peak resident set size of the virtual memory("high water mark")',
                'label': "Virtual Memory High Water Mark",
                'parents': ['pidstatus']
            },

            'VmRSS': {
                'desc': 'Resident set size of the virtual memory',
                'label': "Virtual Memory Resident Size",
                'parents': ['pidstatus']
            },

            'VmData': {
                'desc': 'Size of the data in virtual memory',
                'label': "Virtual Memory Data",
                'parents': ['pidstatus']
            },

            'VmStk': {
                'desc': 'Size of the stack in virtual memory',
                'label': "Virtual Memory Stack",
                'parents': ['pidstatus']
            },

            'VmExe': {
                'desc': 'Size of the text segments in virtual memory',
                'label': "Virtual Memory Text",
                'parents': ['pidstatus']
            },

            'VmLib': {
                'desc': 'Shared library code size of the virtual memory',
                'label': "Virtual Memory Library Code",
                'parents': ['pidstatus']
            },

            'VmPTE': {
                'desc': 'Page table entries size in virtual memory',
                'label': "Virtual Memory Page Table Entries",
                'parents': ['pidstatus']
            },

            'Threads': {
                'desc': 'Number of threads in process containing this thread',
                'label': "Number of Threads",
                'parents': ['pidstatus']
            },

            'SigQ': {
                'desc': 'Contains two slash-separated numbers that relate to queued signals for the real user ID of this process. The first of these is the number of currently queued signals for this real user ID, and the second is the resource limit on the number of queued signals for this process',
                'label': "Queued Signals",
                'parents': ['pidstatus']
            },

            'SigPnd': {
                'desc': 'Number of signals pending for a single thread on its own',
                'label': "Thread Signals Pending",
                'parents': ['pidstatus']
            },

            'ShdPnd': {
                'desc': 'Number of signals pending for process as a whole',
                'label': "Process Signals Pending",
                'parents': ['pidstatus']
            },

            'SigBlk': {
                'desc': 'Mask indicating signals being blocked',
                'label': "Signal Blocked",
                'parents': ['pidstatus']
            },

            'SigIgn': {
                'desc': 'Mask indicating signals being ignored',
                'label': "Signal Ignored",
                'parents': ['pidstatus']
            },

            'SigCgt': {
                'desc': 'Mask indicating signals being caught',
                'label': "Signal Caught",
                'parents': ['pidstatus']
            },

            'CapInh': {
                'desc': 'Mask of capabilities enabled in inheritable sets',
                'label': "Capabilities Inheritable",
                'parents': ['pidstatus']
            },

            'CapPrm': {
                'desc': 'Masks of capabilities enabled in permitted sets',
                'label': "Capabilities Permitted",
                'parents': ['pidstatus']
            },

            'CapEff': {
                'desc': 'Masks of capabilities enabled in effective sets',
                'label': "Capabilities Effective",
                'parents': ['pidstatus']
            },

            'CapBnd': {
                'desc': 'Capability Bounding set ',
                'label': "Capability Bounding",
                'parents': ['pidstatus']
            },

            'Cpus_allowed': {
                'desc': 'Mask of CPUs on which this process may run ',
                'label': "Allowed CPUs",
                'parents': ['pidstatus']
            },

            'Cpus_allowed_list': {
                'desc': 'Mask of CPUs on which this process may run in a "list format',
                'label': "Allowed CPUs List",
                'parents': ['pidstatus']
            },

            'Mems_allowed': {
                'desc': 'Mask of memory nodes allowed to this process',
                'label': "Memory Nodes Allowed",
                'parents': ['pidstatus']
            },

            'Mems_allowed_list': {
                'desc': 'Mask of memory nodes allowed to this process in a "list format"',
                'label': "Memory Nodes Allowed List",
                'parents': ['pidstatus']
            },

            'voluntary_context_switches': {
                'desc': 'Number of voluntary context switches',
                'label': "Voluntary Context Switches",
                'parents': ['pidstatus']
            },

            'nonvoluntary_context_switches': {
                'desc': 'Number of involuntary context switches ',
                'label': "Involuntary Context Switches",
                'parents': ['pidstatus']
            },

        }

        return thevars

    @staticmethod
    def get_data():
        """ Gets parsed /proc/[pid]/status data """
        return PidStatus.parse_pidstatus()

    @staticmethod
    def parse_pidstatus(mode='all'):
        """Parse /proc/[pid]/status for each process

        Result is grouped into pstree-like format. So each group name is PID
        number and each subgroup name also PID number that is connected with
        outer number with parent-child relation.

        Arguments:
            mode (str): how status should be processed

                all - variables and processes relations are collected
                    in hierarchical structure

                flat - same as previous, but hierarchy is not preserved

                relations_only - processes hierarchy is preserved but all
                    variables are skipped
        """

        if mode not in ('flat', 'relations_only', 'all'):
            raise ValueError('incorrect processing mode')

        tabs = re.compile('\s+')
        processes_plain = {'pid': dict()}
        processes_relations = defaultdict(list)

        for status in glob.iglob(PidStatus.PID):
            pid = status.split(os.sep)[2]

            entries = dict()

            for line in open(status):
                parts = [p.strip().replace(':', '') for p in tabs.split(line) if p and p != 'kB']
                k, v = parts[0], ' '.join(parts[1:])
                entries[PidStatus.key_format(k)] = v

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
    ps = PidStatus()
    ps.test_parse()
