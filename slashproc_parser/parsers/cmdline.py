#!/usr/bin/env python

import re
from slashproc_parser.basic_parser import BasicSPParser


class CmdLine(BasicSPParser):
    """ Provides static methods for parsing /proc/cmdline file

        Attributes: CMDLINE (str): path to parsed file
    """

    CMDLINE = "/proc/cmdline"

    def __init__(self):
        super(CmdLine, self).__init__(self)

    @staticmethod
    def get_groups():
        """ Used for getting groups into which file is divided

            Returns: dict: groups
        """
        return {'cmdline': {'label': 'cmdline', 'parents': ['root']}}

    @staticmethod
    def get_vars():
        """ Used for getting variables descriptions from /proc/cmdline

            Each variable is represented by dictionary that contains variable name,
            list of groups that contain this variable and unit of measurement.

            Returns:
                thevars (dict): variables
        """

        descs = {
            'raw': {
                'desc': "The full kernel boot command",
                'label': "Command Kernel Line",
                'parents': ['cmdline']
            },

            'boot_image': {
                'desc': '',
                'label': "Boot Image",
                'parents': ['cmdline']
            },

            'console': {
                'desc': 'Outputs console device and options',
                'label': "Console",
                'parents': ['cmdline']
            },

            'netconsole': {
                'desc': 'Sends kernel console data across the network using UDP packets to another machine',
                'label': "Net Console",
                'parents': ['cmdline']
            },

            'debug': {
                'desc': 'Causes the kernel log level to be set to the debug level, so that all debug messages will be printed to the console at boot time',
                'label': "Debug",
                'parents': ['cmdline']
            },

            'earlyprintk': {
                'desc': 'Shows kernel log messages that precede the initialization of the traditional console',
                'label': "Early Print",
                'parents': ['cmdline']
            },

            'loglevel': {
                'desc': 'Specifies log level. Any log messages with levels less than this will be printed to the console',
                'label': "Log Level",
                'parents': ['cmdline']
            },

            'log_buf_len': {
                'desc': 'Sets the size of internal log buffer of the kernel. Must be a power of 2',
                'label': "Log buffer Length",
                'parents': ['cmdline']
            },

            'initcall_debug': {
                'desc': 'Causes the kernel to trace all functions that are called by the kernel during initialization of the system as the kernel boots',
                'label': "InitCall Debug",
                'parents': ['cmdline']
            },

            'kstack': {
                'desc': 'Specifies how many words from the kernel stack should be printed in the kernel oops dumps. Must be integer',
                'label': "Kernel Stack",
                'parents': ['cmdline']
            },

            'time': {
                'desc': 'Causes the kernel to prefix every kernel log message with a timestamp',
                'label': "Time Stamp",
                'parents': ['cmdline']
            },

            'apic': {
                'desc': 'Controls how much information the APIC subsystem generates when booting the kernel',
                'label': "APIC verbosity",
                'parents': ['cmdline']
            },

            'noapic': {
                'desc': 'Prevents the kernel from using any of the IOAPICs that might be present in the system',
                'label': "No APIC",
                'parents': ['cmdline']
            },

            'lapic': {
                'desc': 'Cause the kernel to enable the local APIC even if the BIOS had disabled it',
                'label': "Local APIC",
                'parents': ['cmdline']
            },

            'nolapic': {
                'desc': 'Tell the kernel not to use the local APIC',
                'label': "No local APIC",
                'parents': ['cmdline']
            },

            'noirqbalance': {
                'desc': 'Disables all of the built-in kernel IRQ balancing logic',
                'label': "No IRQ Balance",
                'parents': ['cmdline']
            },

            'irqfixup': {
                'desc': 'Basic fix to interrupt problems',
                'label': "IRQ Basic Fix-up",
                'parents': ['cmdline']
            },

            'irqpoll': {
                'desc': 'Extended fix to interrupt problems',
                'label': "IRQ Extended Fix-up",
                'parents': ['cmdline']
            },

            'noirqdebug': {
                'desc': 'Disables unhandled interrupt detection',
                'label': "No Unhandled Interrupt Detection",
                'parents': ['cmdline']
            },

            'highmem': {
                'desc': 'Forces the highmem memory zone to have an exact size of n bytes',
                'label': "Highmem Size",
                'parents': ['cmdline']
            },

            'hugepages': {
                'desc': 'Lets Linux to use 4MB pages, one thousand times the default size. Sets the maximum number of hugetlb pages',
                'label': "Number of Huge Pages",
                'parents': ['cmdline']
            },

            'ihash_entries': {
                'desc': 'Overrides the default number of hash buckets for the inode cache of the kernel',
                'label': "Inode Cache",
                'parents': ['cmdline']
            },

            'max_addr': {
                'desc': 'Causes the kernel to ignore all physical memory greater than or equal to the physical address',
                'label': "Ignore Memory",
                'parents': ['cmdline']
            },

            'mem': {
                'desc': 'Sets the specific ammount of memory used by the kernel',
                'label': "Force Memory Usage",
                'parents': ['cmdline']
            },

            'memmap': {
                'desc': 'Uses a specific memory map. The exactmap lines can be constructed based on BIOS output or other requirements',
                'label': "E820 Memory Map",
                'parents': ['cmdline']
            },

            'noexec': {
                'desc': 'Enables or disables the ability of the kernel to map sections of memory as non-executable. ',
                'label': "Non-Executable Mappings",
                'parents': ['cmdline']
            },

            'reserve': {
                'desc': 'Forces the kernel to ignore some of the I/O memory areas',
                'label': "Reserve I/O Memory",
                'parents': ['cmdline']
            },

            'vmalloc': {
                'desc': 'Forces vmalloc to have the exact size. This can be used to increase or decrease the size of the vmalloc area ',
                'label': "Size of VMalloc",
                'parents': ['cmdline']
            },

            'norandmaps': {
                'desc': 'Disables randomization of the address space of all programs when they are started',
                'label': "Address Space Randomization",
                'parents': ['cmdline']
            },

            'vdso': {
                'desc': 'Enables or disables the VDSO (virtual dynamically linked shared objects) mapping',
                'label': "VDSO Mapping",
                'parents': ['cmdline']
            },

            'resume': {
                'desc': 'Tells the kernel which disk device contains the suspended kernel image. Kernel image created by the software suspend subsystem will be loaded into memory and run instead of the normal boot process',
                'label': "Partition Device for the Suspend Image",
                'parents': ['cmdline']
            },

            'noresume': {
                'desc': 'Disables the resume functionality of the kernel. Any swap partitions that were being used to hold system images to which the kernel could be restored will revert back to available swap space',
                'label': "Disable Resume",
                'parents': ['cmdline']
            },

            'ro': {
                'desc': "Mount root device read-only on boot",
                'label': "Kernel Permissions",
                'parents': ['cmdline']
            },

            'root': {
                'desc': "Location of the root filesystem image",
                'label': 'Root directory',
                'parents': ['cmdline']
            },

            'rhgb': {
                'desc': "Red Hat Graphical Boot. Graphical booting is supported",
                'label': 'Graphical Boot',
                'parents': ['cmdline']
            },

            'quiet': {
                'desc': "All verbose kernel messages except extremely serious should be suppressed at boot time",
                'label': 'Suppress boot messages',
                'parents': ['cmdline']
            },

            'lang': {
                'desc': "Language",
                'label': 'Language',
                'parents': ['cmdline']
            },
        }

        # remove not appeared in cmd arguments
        thevars = dict()
        for var in CmdLine.get_data():
            if var in descs:
                thevars[var] = descs[var]

        return thevars

    @staticmethod
    def get_data():
        """ Parse /proc/cmdline. All variables are stored in single group.

            Returns: data (dict): dictionary with variables and their values
        """
        retdict = dict()

        with open(CmdLine.CMDLINE) as f:
            line = f.readline().strip('\n')
            retdict['raw'] = line

            for arg in line.split():

                if re.match('[\w_.]+=', arg):
                    pos = arg.find('=')
                    k, v = arg[:pos], arg[pos+1:]
                    retdict[CmdLine.key_format(k)] = v

                else:
                    retdict[CmdLine.key_format(arg)] = arg

        return retdict

if __name__ == "__main__":
    cl = CmdLine()
    cl.test_parse()
