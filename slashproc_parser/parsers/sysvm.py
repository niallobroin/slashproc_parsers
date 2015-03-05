#!/usr/bin/env python

from slashproc_parser.basic_parser import BasicSPParser
from parse_helpers import traverse_directory


class Vm(BasicSPParser):

    VM = "/proc/sys/vm"

    @staticmethod
    def get_groups():
        """Enumerates groups depending on number of directories in /proc/sys/vm.

        Returns:
            groups (dict): parsed variables groups
        """
        _, parents, all_variables = traverse_directory(Vm.VM)

        # no need to take into account variables
        for var in all_variables:
            del parents[var]

        groups = {'sysvm': {'label': 'Virtual memory system variables', 'parents': ['root']}}

        for i in parents.keys():
            groups[Vm.key_format(i)] = {
                'label': i,
                'desc': '',
                'parents': parents[i]
            }

        return groups

    @staticmethod
    def get_vars():
        """Enumerates system variables in /proc/sys/vm and its subdirectories.

        Returns:

        """
        thevars = dict()
        _, parents, all_variables = traverse_directory(Vm.VM)

        for var in all_variables:
            thevars[Vm.key_format(var)] = {
                'label': var,
                'unit': '',
                'parents': parents[var]
            }

        # TODO: fill with variables and appropriate descriptions
        descs = [
            ('block_dump', '', ''),
            ('dirty_background_ratio', '', ''),
            ('dirty_expire_centisecs', '', ''),
            ('dirty_ratio', '', ''),
            ('dirty_writeback_centisecs', '', ''),
            ('laptop_mode', '', ''),
            ('max_map_count', '', ''),
            ('min_free_kbytes', '', ''),
            ('nr_hugepages', '', ''),
            ('nr_pdflush_threads', '', ''),
            ('', '', ''),
            ('', '', ''),
            ('', '', ''),
        ]

        return thevars

    @staticmethod
    def get_data(verbose=False):
        """Parse /proc/sys/vm directory and its subdirs.

        Each non-directory file name is treated as variable name. Accordingly,
        file's content is treated as variable value. All groups in result
        dictionary preserve parent-child relations.

        Returns:
            tree (dict): nested dictionaries with system variables
        """
        tree, _, _ = traverse_directory(Vm.VM, verbose=verbose)
        return tree


if __name__ == "__main__":
    vm = Vm()
    vm.test_parse()