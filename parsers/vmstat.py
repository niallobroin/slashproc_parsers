#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser


class VmStat(BasicSPParser):
    """
    Provides static methods for parsing /proc/vmstat file

    Attributes:
        VMSTAT (str): path to parsed file
    """

    VMSTAT = "/proc/vmstat"

    def __init__(self):
        super(VmStat, self).__init__(self)

    @staticmethod
    def get_groups():
        """Used for getting groups into which file is divided

        Returns:
            dict: groups
        """
        return {'vmstat': {'label': 'vmstat', 'parents': ['root']}}

    @staticmethod
    def get_vars():
        """Used for getting variables descriptions from /proc/vmstat

        Each variable is represented by dictionary that contains variable name,
        list of groups that contain this variable and unit of measurement.

        Returns:
            thevars (dict): variables

        """
        retdict = VmStat.get_data()
        thevars = dict()
        for i in retdict.keys():
            thevars[VmStat.key_format(i)] = {
                'label': i,
                'unit': '',
                'parents': ['vmstat']
            }

        descs = {
            ('nr_dirty', 'Number of dirty pages', ''),
            ('nr_writeback', 'Number of pages that are under writeback', ''),
            ('nr_unstable', 'Number of unstable pages', ''),
            ('nr_page_table_pages', 'Number of pages allocated to page tables', ''),
            ('nr_mapped', 'Number of pages mapped to files', ''),
            ('nr_slab', 'Number of pages allocated by the kernel', ''),
            ('pgpgin', 'Number of pageins since the last boot', ''),
            ('pgpgout', 'Number of pageouts since the last boot', ''),
            ('pswpin', 'Number of swapins since the last boot', ''),
            ('pswpout', 'Number of swapouts since the last boot', ''),
            # Number of page allocations per zone (need more specific description)
            ('pgalloc_high', '', ''),
            ('pgalloc_normal', '', ''),
            ('pgalloc_dma32', '', ''),
            ('pgalloc_dma', '', ''),
            ('pgfree', 'Number of page frees since the last boot', ''),
            ('pgactivate', 'Number of page activations since the last boot', ''),
            ('pgdeactivate', 'Number of page deactivations since the last boot', ''),
            ('pgdefault', 'Number of minor page faults since the last boot', ''),
            ('pgmajfault', 'Number of major page faults since the last boot', ''),
            # Number of page refills per zone
            ('pgrefill_high', '', ''),
            ('pgrefill_normal', '', ''),
            ('pgrefill_dma32', '', ''),
            ('pgrefill_dma', '', ''),
            # Number of page steals
            ('pgsteal_high', '', ''),
            ('pgsteal_normal', '', ''),
            ('pgsteal_dma32', '', ''),
            ('pgsteal_dma', '', ''),
            # Number of pages scanned by the kswapd daemon per zone
            ('pgscan_kswapd_high', '', ''),
            ('pgscan_kswapd_normal', '', ''),
            ('pgscan_kswapd_dma32', '', ''),
            ('pgscan_kswapd_dma', '', ''),
            # Number of pages reclaimed directly
            ('pgscan_direct_high', '', ''),
            ('pgscan_direct_normal', '', ''),
            ('pgscan_direct_dma32', '', ''),
            ('pgscan_direct_dma', '', ''),
            ('pginodesteal', 'Number of pages reclaimed via inode freeing since the last boot', ''),
            ('slabs_scanned', 'Number of slab objects scanned since the last boot', '')
        }

        for var, desc, unit in descs:
            if var in thevars:
                thevars[var]['desc'] = desc
                thevars[var]['unit'] = unit
        return thevars

    @staticmethod
    def get_data():
        """
        Parse /proc/vmstat. All variables are stored in single group.

        Returns:
            stats (dict): dictionary with variables and their values
        """
        stats = dict()
        for l in open(VmStat.VMSTAT):
            line = l.split()
            if len(line) == 2:
                k = line[0].strip().replace('\t', '').replace('\n', '').lower()
                v = line[1].strip().replace('\t', '').replace('\n', '').lower()
                stats[k] = int(v)
        return stats


if __name__ == "__main__":
    vm = VmStat()
    vm.test_parse()
