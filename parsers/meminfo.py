#!/usr/bin/env python

import re
from sp_parser.basic_sp_parser import BasicSPParser


class MemInfo(BasicSPParser):

    MEMINFO = "/proc/meminfo"

    def __init__(self):
        super(MemInfo, self).__init__(self)

    @staticmethod
    def get_groups():
        """
        Static method to define groups that that parser can parse
        """
        return {'meminfo': {'label': 'Memory Information',
                            'parents': ['root']}}

    @staticmethod
    def get_vars():
        """
        Static method to define vars that that parser can parse
        """
        thevars = {
            'memtotal': {'label': "MemTotal", 'desc': "Total amount of physical RAM, in kilobytes."},
            'memfree': {'label': "MemFree", 'desc': "The amount of physical RAM, in kilobytes, left unused by the system."},
            'buffers': {'label': "Buffers", 'desc': "The amount of physical RAM, in kilobytes, used for file buffers."},
            'cached': {'label': "Cached", 'desc': "The amount of physical RAM, in kilobytes, used as cache memory."},
            'swapcached': {'label': "SwapCached", 'desc': "The amount of swap, in kilobytes, used as cache memory."},
            'active': {'label': "Active", 'desc': "The total amount of buffer or page cache memory, in kilobytes, that is in active use. This is memory that has been recently used and is usually not reclaimed for other purposes."},
            'inactive': {'label': "Inactive", 'desc': "The total amount of buffer or page cache memory, in kilobytes, that are free and available. This is memory that has not been recently used and can be reclaimed for other purposes."},
            #: {'label': "HighTotal and HighFree", 'desc': "The total and free amount of memory, in kilobytes, that is not directly mapped into kernel space. The HighTotal value can vary based on the type of kernel used."},
            #: {'label': "LowTotal and LowFree", 'desc': "The total and free amount of memory, in kilobytes, that is directly mapped into kernel space. The LowTotal value can vary based on the type of kernel used."},
            'swaptotal': {'label': "SwapTotal", 'desc': "The total amount of swap available, in kilobytes."},
            'swapfree': {'label': "SwapFree", 'desc': "The total amount of swap free, in kilobytes."},
            'dirty': {'label': "Dirty", 'desc': "The total amount of memory, in kilobytes, waiting to be written back to the disk."},
            'writeback': {'label': "Writeback", 'desc': "The total amount of memory, in kilobytes, actively being written back to the disk."},
            'mapped': {'label': "Mapped", 'desc': "The total amount of memory, in kilobytes, which have been used to map devices, files, or libraries using the mmap command."},
            'slab': {'label': "Slab", 'desc': "The total amount of memory, in kilobytes, used by the kernel to cache data structures for its own use."},
            'committed_as': {'label': "Committed_AS", 'desc': "The total amount of memory, in kilobytes, estimated to complete the workload. This value represents the worst case scenario value, and also includes swap memory."},
            'pagetables': {'label': "PageTables", 'desc': "The total amount of memory, in kilobytes, dedicated to the lowest page table level."},
            'vmalloctotal': {'label': "VMallocTotal", 'desc': "The total amount of memory, in kilobytes, of total allocated virtual address space."},
            'vmallocused': {'label': "VMallocUsed", 'desc': "The total amount of memory, in kilobytes, of used virtual address space."},
            'vmallocchunk': {'label': "VMallocChunk", 'desc': "The largest contiguous block of memory, in kilobytes, of available virtual address space."},
            'hugepages_total': {'label': "HugePages_Total", 'desc': "The total number of hugepages for the system. The number is derived by dividing Hugepagesize by the megabytes set aside for hugepages specified in /proc/sys/vm/hugetlb_pool. This statistic only appears on the x86, Itanium, and AMD64 architectures."},
            'hugepages_free': {'label': "HugePages_Free", 'desc': "The total number of hugepages available for the system. This statistic only appears on the x86, Itanium, and AMD64 architectures."},
            'hugepagesize': {'label': "Hugepagesize", 'desc': "The size for each hugepages unit in kilobytes. By default, the value is 4096 KB on uniprocessor kernels for 32 bit architectures. For SMP, hugemem kernels, and AMD64, the default is 2048 KB. For Itanium architectures, the default is 262144 KB. This statistic only appears on the x86, Itanium, and AMD64 architectures."},
        }
        for i in MemInfo.get_data()['meminfo']:
            if i not in thevars:
                thevars[MemInfo.key_format(i)] = {'label': i,
                                                  'unit': 'kB',
                                                  'parents': ['meminfo']}
            else:
                thevars[i]['unit'] = 'KB'
                thevars[i]['parents'] = ['meminfo']


        return thevars

    @staticmethod
    def get_data():
        """
        Collects the /proc/meminfo
        """
        
        memcache = dict()
        re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB')
        for line in open(MemInfo.MEMINFO):
            match = re_parser.match(line)
            if not match:
                continue # skip lines that don't parse
            k, v = match.groups(['key', 'value'])
            memcache[MemInfo.key_format(k)] = int(v)
        
            
        return {'meminfo': memcache}



if __name__ == "__main__":
    c = MemInfo()
    c.test_parse()






