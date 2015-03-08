#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser
from parse_helpers import traverse_directory


class Kernel(BasicSPParser):

    KERNEL = "/proc/sys/kernel"

    @staticmethod
    def get_groups():
        """Enumerates groups depending on number of directories in /proc/sys/kernel.

        Returns:
            groups (dict): parsed variables groups
        """
        _, parents, all_variables = traverse_directory(Kernel.KERNEL)

        # no need to take into account variables
        for var in all_variables:
            del parents[var]

        groups = {'syskernel': {'label': 'Kernel system variables', 'parents': ['root']}}

        for i in parents.keys():
            groups[Kernel.key_format(i)] = {
                'label': i,
                'desc': '',
                'parents': parents[i]
            }

        return groups

    @staticmethod
    def get_vars():
        """Enumerates system variables in /proc/sys/kernel and its subdirectories.

        Returns:
            thevars (dict): parsed system variables with their descriptions
        """
        thevars = dict()
        _, parents, all_variables = traverse_directory(Kernel.KERNEL)

        for var in all_variables:
            thevars[Kernel.key_format(var)] = {
                'label': var,
                'unit': '',
                'parents': parents[var]
            }

        # TODO: fill with variables and appropriate descriptions
        descs = [
            ('acct', '', ''),
            ('ctrl_alt_del', '', ''),
            ('domainname', '', ''),
            ('exec_shield', '', ''),
            ('hostname', '', ''),
            ('hotplug', '', ''),
            ('modprobe', '', ''),
            ('msgmax', '', ''),
            ('msgmnb', '', ''),
            ('msgmni', '', ''),
            ('osrelease', '', ''),
            ('ostype', '', ''),
            ('overflowgid', '', ''),
            ('overflowuid', '', ''),
            ('panic', '', ''),
            ('printk', '', ''),
            ('sem', '', ''),
            ('shmall', '', ''),
            ('', '', ''),
            ('', '', ''),
            ('', '', ''),
        ]

        return thevars

    @staticmethod
    def get_data(verbose=False):
        """Parse /proc/sys/kernel directory and its subdirs.

        Each non-directory file name is treated as variable name. Accordingly,
        file's content is treated as variable value. All groups in result
        dictionary preserve parent-child relations.

        Returns:
            tree (dict): nested dictionaries with system variables
        """

        tree, _, _ = traverse_directory(Kernel.KERNEL, verbose=verbose)
        return tree


if __name__ == "__main__":
    k = Kernel()
    k.test_parse()
