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
        descs = {
            'raw': {
                'desc': "The full sys/vm log",
                'label': "Sys VM Full",
                'parents': ['vm']
            },
            
            'block_dump': {
                'desc': "Enables block I/O debugging when set to a nonzero value. If you want to find out which process caused the disk to spin up (see /proc/sys/vm/laptop_mode), you can gather information by setting the flag",
                'label': "Block Dump I/O Debugging",
                'parents': ['vm']
            },
            
            'dirty_background_bytes': {
                'desc': "Contains the amount of dirty memory at which the pdflush background writeback daemon will start writeback",
                'label': "Dirty Background Bytes",
                'parents': ['vm']
            },
            
            'dirty_background_ratio': {
                'desc': "Contains, as a percentage of total system memory, the number of pages at which the pdflush background writeback daemon will start writing out dirty data",
                'label': "Dirty Background Ratio",
                'parents': ['vm']
            },
            
            'dirty_bytes': {
                'desc': "Contains the amount of dirty memory at which a process generating disk writes will itself start writeback",
                'label': "Dirty Bytes",
                'parents': ['vm']
            },
            
            'dirty_expire_centisecs': {
                'desc': "Used to define when dirty data is old enough to be eligible for writeout by the pdflush daemons. It is expressed in 100'ths of a second. Data which has been dirty in memory for longer than this interval will be written out next time a pdflush daemon wakes up",
                'label': "Dirty Expire Centisecs",
                'parents': ['vm']
            },
            
            'dirty_ratio': {
                'desc': "Contains, as a percentage of total system memory, the number of pages at which a process which is generating disk writes will itself start writing out dirty data",
                'label': "Dirty Ratio",
                'parents': ['vm']
            },
            
            'dirty_writeback_centisecs': {
                'desc': "The pdflush writeback daemons will periodically wake up and write "old" data out to disk. This tunable expresses the interval between those wakeups, in 100'ths of a second",
                'label': "Dirty Writeback Centisecs",
                'parents': ['vm']
            },
            
            'drop_caches': {
                'desc': "Causes the kernel to drop clean caches, dentries and inodes from memory, causing that memory to become free",
                'label': "Drop Caches",
                'parents': ['vm']
            },
            
            'highmem_is_dirtyable': {
                'desc': "This defaults to 0 (false), meaning that the dirty_ratio and dirty_background_ratio ratios are calculated as a percentage of low memory only. This protects against excessive scanning in page reclaim, swapping and general VM distress",
                'label': "HighMem is Dirtyable",
                'parents': ['vm']
            },
            
            'hugepages_treat_as_movable': {
                'desc': "Huge pages are not movable so are not allocated from ZONE_MOVABLE by default. However, as ZONE_MOVABLE will always have pages that can be migrated or reclaimed, it can be used to satisfy hugepage allocations even when the system has been running a long time. This allows an administrator to resize the hugepage pool at runtime depending on the size of ZONE_MOVABLE",
                'label': "Huge Pages Treated as Movable ",
                'parents': ['vm']
            },
            
            'hugetlb_shm_group': {
                'desc': "Contains group id that is allowed to create SysV shared memory segment using hugetlb page",
                'label': "HugeTLB Shared Memory Group",
                'parents': ['vm']
            },
            
            'laptop_mode': {
                'desc': "A knob that controls 'laptop mode'. When the knob is set, any physical disk I/O (that might have caused the hard disk to spin up, see /proc/sys/vm/block_dump) causes Linux to flush all dirty blocks",
                'label': "Laptop Mode",
                'parents': ['vm']
            },
            
            'legacy_va_layout': {
                'desc': "If non-zero, this sysctl disables the new 32-bit mmap map layout - the kernel will use the legacy (2.4) layout for all processes",
                'label': "Disable 32-bit MMAP Layout",
                'parents': ['vm']
            },
            
            'lowmem_reserve_ratio': {
                'desc': "Ratio of total pages to free pages for each memory zone",
                'label': "Low Memory Reserve Ratio",
                'parents': ['vm']
            },
            
            'max_map_count': {
                'desc': "Maximum number of memory map areas a process may have. Memory map areas are used as a side-effect of calling malloc, directly by mmap and mprotect, and also when loading shared libraries",
                'label': "Maximum Number of Memory Map Areas",
                'parents': ['vm']
            },
            
            'min_free_kbytes': {
                'desc': "Used to force the Linux VM to keep a minimum number of kilobytes free. The VM uses this number to compute a pages_min value for each lowmem zone in the system. Each lowmem zone gets a number of reserved free pages based proportionally on its size",
                'label': "Mininum Free KBytes",
                'parents': ['vm']
            },
            
            'min_slab_ratio': {
                'desc': "A percentage of the total pages in each zone. On Zone reclaim (fallback from the local zone occurs) slabs will be reclaimed if more than this percentage of pages in a zone are reclaimable slab pages. This insures that the slab growth stays under control even in NUMA systems that rarely perform global reclaim",
                'label': "Minimum Slab Ratio",
                'parents': ['vm']
            },
            
            'min_unmapped_ratio': {
                'desc': "A percentage of the total pages in each zone. Zone reclaim will only occur if more than this percentage of pages are in a state that zone_reclaim_mode allows to be reclaimed",
                'label': "Minimum Unmapped Ratio",
                'parents': ['vm']
            },
            
            'mmap_min_addr': {
                'desc': "Indicates the amount of address space which a user process will be restricted from mmaping. Since kernel null dereference bugs could accidentally operate based on the information in the first couple of pages of memory userspace processes should not be allowed to write to them",
                'label': "MMAP Minimal Address",
                'parents': ['vm']
            },
            
            'nr_hugepages': {
                'desc': "Indicates the current number of configured hugetlb pages in the kernel. Super user can dynamically request more (or free some pre-configured) hugepages. The allocation (or deallocation) of hugetlb pages is possible only if there are enough physically contiguous free pages in system (freeing of hugepages is possible only if there are enough hugetlb pages free that can be transferred back to regular memory pool)",
                'label': "Number of HugePages",
                'parents': ['vm']
            },
            
            'nr_overcommit_hugepages': {
                'desc': "Changes the maximum size of the hugepage pool. The maximum is nr_hugepages + nr_overcommit_hugepages",
                'label': "OverCommit Number of HugePages",
                'parents': ['vm']
            },
            
            'nr_pdflush_threads': {
                'desc': "The count of currently-running pdflush threads. This is a read-only value",
                'label': "Number of PDFlush Threads",
                'parents': ['vm']
            },
            
            'nr_trim_pages': {
                'desc': "This value adjusts the excess page trimming behaviour of power-of-2 aligned NOMMU mmap allocations",
                'label': "Number of Trim Pages",
                'parents': ['vm']
            },
            
            'numa_zonelist_order': {
                'desc': "This sysctl is only for NUMA. It specifies where the memory is allocated from and is controlled by zonelists",
                'label': "Numa ZoneList Order",
                'parents': ['vm']
            },
            
            'oom_dump_tasks': {
                'desc': "Enables a system-wide task dump (excluding kernel threads) to be produced when the kernel performs an OOM-killing and includes such information as pid, uid, tgid, vm size, rss, cpu, oom_adj score, and name. This is helpful to determine why the OOM killer was invoked and to identify the rogue task that caused it",
                'label': "Out-Of-Memory Dump Tasks",
                'parents': ['vm']
            },
            
            'oom_kill_allocating_task': {
                'desc': "Enables or disables killing the OOM-triggering task in out-of-memory situations",
                'label': "Kill Out-Of-Memory Dump Task",
                'parents': ['vm']
            },
            
            'overcommit_memory': {
                'desc': "Controls overcommit of system memory, possibly allowing processes to allocate (but not use) more memory than is actually available",
                'label': "OverCommit Memory",
                'parents': ['vm']
            },
            
            'overcommit_ratio': {
                'desc': "Percentage of physical memory size to include in overcommit calculations",
                'label': "OverCommit Ratio",
                'parents': ['vm']
            },
            
            'page-cluster': {
                'desc': "Controls the number of pages which are written to swap in a single attempt. The swap I/O size",
                'label': "Page Cluster",
                'parents': ['vm']
            },
            
            'panic_on_oom': {
                'desc': "Enables or disables panic on out-of-memory feature. If this is set to 1, the kernel panics when out-of-memory happens. If this is set to 0, the kernel will kill some rogue process, by calling oom_kill()",
                'label': "Panic on Out-Of-Memory",
                'parents': ['vm']
            },
            
            'percpu_pagelist_fraction': {
                'desc': "This is the fraction of pages at most (high mark pcp->high) in each zone that are allocated for each per cpu page list. The min value for this is 8. It means that we don't allow more than 1/8th of pages in each zone to be allocated in any single per_cpu_pagelist",
                'label': "PageList Fraction Per CPU",
                'parents': ['vm']
            },
            
            'scan_unevictable_pages': {
                'desc': "Initiates a scan of individual or all zones' unevictable lists and move any pages that have become evictable onto the respective zone's inactive list, where shrink_inactive_list() will deal with them. If evictable pages are found in unevictable lru, kernel will print filenames and file offsets of those pages",
                'label': "Scan Unevictable Pages",
                'parents': ['vm']
            },
            
            'stat_interval': {
                'desc': "Configures VM statistics update interval. The default value is 1. This tunable first appeared in 2.6.22 kernel",
                'label': "VM Statistics Update Interval",
                'parents': ['vm']
            },
            
            'swap_token_timeout': {
                'desc': "Contains valid hold time of swap out protection token. The Linux VM has token based thrashing control mechanism and uses the token to prevent unnecessary page faults in thrashing situation. The unit of the value is second. The value would be useful to tune thrashing behavior",
                'label': "Swap Token TimeOut",
                'parents': ['vm']
            },
            
            'swappiness': {
                'desc': "Sets the kernel's balance between reclaiming pages from the page cache and swapping process memory. The default value is 60. If you want kernel to swap out more process memory and thus cache more file contents increase the value. Otherwise, if you would like kernel to swap less decrease it",
                'label': "Swappiness",
                'parents': ['vm']
            },
            
            'vdso_enabled': {
                'desc': "When this flag is set, the kernel maps a vDSO page into newly created processes and passes its address down to glibc upon exec(). This feature is enabled by default",
                'label': "vDSO Enabled",
                'parents': ['vm']
            },
            
            'vfs_cache_pressure': {
                'desc': "Controls the tendency of the kernel to reclaim the memory which is used for caching of directory and inode objects",
                'label': "VFS Cache Pressure",
                'parents': ['vm']
            },
            
            'zone_reclaim_mode': {
                'desc': "Allows someone to set more or less aggressive approaches to reclaim memory when a zone runs out of memory. If it is set to zero then no zone reclaim occurs. Allocations will be satisfied from other zones / nodes in the system",
                'label': "Zone Reclaim Mode",
                'parents': ['vm']
            },
            
        }
 
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