#!/usr/bin/env python

from slashproc_parser.basic_parser import BasicSPParser
from parse_helpers import traverse_directory


class SysKernel(BasicSPParser):

    KERNEL = "/proc/sys/kernel"

    @staticmethod
    def get_groups():
        """Enumerates groups depending on number of directories in /proc/sys/kernel.

        Returns:
            groups (dict): parsed variables groups
        """
        _, parents, all_variables = traverse_directory(SysKernel.KERNEL)

        # no need to take into account variables
        for var in all_variables:
            del parents[var]

        groups = {'syskernel': {'label': 'SysKernel system variables', 'parents': ['root']}}

        for i in parents.keys():
            groups[SysKernel.key_format(i)] = {
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
        _, parents, all_variables = traverse_directory(SysKernel.KERNEL)

        for var in all_variables:
            thevars[SysKernel.key_format(var)] = {
                'label': var,
                'unit': '',
                'parents': parents[var]
            }

        # TODO: fill with variables and appropriate descriptions
        descs = {
            'acct': {
                'desc': "BSD-style process accounting is enabled. It contains three values; highwater, lowwater, and frequency. These values control process accounting behavior. If the free space on the file system where the log lives goes below lowwater percentage, accounting suspends. If it goes above highwater percentage, accounting resumes. Frequency determines how often (in seconds) you check the amount of free space",
                'label': "BSD-Style Process Accounting",
                'parents': ['SysKernel']
            },

            'acpi_video_flags': {
                'desc': "Allows mode of video boot to be set during run time",
                'label': "ACPI Video Flags",
                'parents': ['SysKernel']
            },

            'bootloader_type': {
                'desc': "Exports to userspace the boot loader ID which has been exported by (b)zImage boot loaders since boot protocol version 2",
                'label': "BootLoader Type",
                'parents': ['SysKernel']
            },
            
            'cad_pid': {
                'desc': "Allows to set/get PID of the process that gets the signal when ctrl-alt-del key sequence is pressed. By default it is the init process (PID 1)",
                'label': "Set/Get PID",
                'parents': ['SysKernel']
            },
            
            'cap-bound': {
                'desc': "Exports the so called capability bounding set to userspace: a list of capabilities that are allowed to be held by any process on the system. If a capability does not appear in the bounding set, it may not be exercised by any process, no matter how privileged",
                'label': "Capability Bounding Set",
                'parents': ['SysKernel']
            },
            
            'core_pattern': {
                'desc': "Specifies a core dumpfile pattern name",
                'label': "Dumpfile Pattern Name",
                'parents': ['SysKernel']
            },
            
            'core_uses_pid': {
                'desc': "By setting core_uses_pid to 1 (the default is 0), the coredump filename becomes core",
                'label': "Core Uses Pid",
                'parents': ['SysKernel']
            },
            
            'ctrl-alt-del': {
                'desc': "Allows init program to handle a graceful restart (or to the PID of your choice, which you can configure with cad_pid tunable) in case the value = 0 or and immediate restart if the value >0",
                'label': "Ctrl-Alt-Del",
                'parents': ['SysKernel']
            },
            
            'domainname': {
                'desc': "Sets the NIS/YP domainname in exactly the same way as the command domainname",
                'label': "Domain Name",
                'parents': ['SysKernel']
            },
            
            'hostname': {
                'desc': "Sets the NIS/YP hostname in exactly the same way as the command hostname",
                'label': "Host Name",
                'parents': ['SysKernel']
            },
            
            'hotplug': {
                'desc': "The location where the hotplug policy agent is located. The default value is /sbin/hotplug",
                'label': "Location of HotPlug",
                'parents': ['SysKernel']
            },
            
            'hz_timer': {
                'desc': "Switches the regular HZ timer off when the system is going idle. This helps z/VM to detect that the Linux system is idle. VM can then swap out this guest which reduces memory usage. It also reduces the overhead of idle systems",
                'label': "HZ Timer Switcher",
                'parents': ['SysKernel']
            },
            
            'ieee_emulation_warnings': {
                'desc': "Reports IEEE floating point warnings",
                'label': "IEEE Emulation Warnings",
                'parents': ['SysKernel']
            },
            
            'kstack_depth_to_print': {
                'desc': "Controls the number of words to print when dumping the raw kernel stack. The default value depends on the CPU architecture",
                'label': "SysKernel Stack Print Depth",
                'parents': ['SysKernel']
            },
            
            'maps_protect': {
                'desc': "Enables/disables the protection of the per-process proc entries maps and smaps. When enabled, the contents of these files are visible only to readers that are allowed to ptrace() the given process",
                'label': "Maps/Smaps Protection",
                'parents': ['SysKernel']
            },
            
            'max_lock_depth': {
                'desc': "Limits the amount of deadlock-checking the kernel will do. The default value is 1024",
                'label': "DeadLock Checking Limit",
                'parents': ['SysKernel']
            },
            
            'modprobe': {
                'desc': "The location where the modprobe binary is located. The kernel uses this program to load modules on demand. The default value is /sbin/modprobe",
                'label': "ModProbe Location",
                'parents': ['SysKernel']
            },
            
            'msgmax': {
                'desc': "Specifies the maximum allowable size of any single message in a System V IPC message queue, in bytes. msgmax must be no larger than msgmnb (the size of a queue). The default is 8192 bytes",
                'label': "Maximum Size of a Message",
                'parents': ['SysKernel']
            },
            
            'msgmnb': {
                'desc': "Specifies the maximum allowable total combined size of all messages queued in a single given System V IPC message queue at any one time, in bytes. The default is 16384 bytes",
                'label': "Maximum Total Messages Size",
                'parents': ['SysKernel']
            },
            
            'msgmni': {
                'desc': "Specifies the maximum number of system-wide System V IPC message queue identifiers (one per queue). The default is 16",
                'label': "Maximum Number of Message Queue Identifiers",
                'parents': ['SysKernel']
            },
            
            'ngroups_max': {
                'desc': "Specifies  the maximum number of supplementary groups a user can be a member of (kernel's NGROUPS_MAX) to the userspace. The default value is 65536. This tunable does not seem to be used anywhere in the latest kernels",
                'label': "Maximum number of Supplementary Groups",
                'parents': ['SysKernel']
            },
            
            'nmi_watchdog': {
                'desc': "Enables/disables NMI watchdog. It is enabled by default on configurations that supports it",
                'label': "NWI WatchDog",
                'parents': ['SysKernel']
            },
            
            'osrelease': {
                'desc': "The running kernel version",
                'label': "OS Release",
                'parents': ['SysKernel']
            },
            
            'ostype': {
                'desc': "The running OS type",
                'label': "OS Type",
                'parents': ['SysKernel']
            },
            
            'overflowgid': {
                'desc': "Specifies GID. This sysctl allows to change the value of the fixed GID. The default is 65534",
                'label': "Specify GID",
                'parents': ['SysKernel']
            },
            
            'overflowuid': {
                'desc': "Specifies UID. This sysctl allows you to change the value of the fixed UID. The default is 65534",
                'label': "Specify UID",
                'parents': ['SysKernel']
            },
            
            'panic': {
                'desc': "Represents the number of seconds the kernel waits before rebooting on a panic. When you use the software watchdog, the recommended setting is 60. If set to 0, the auto reboot after a kernel panic is disabled, which is the default setting",
                'label': "Time Before Panic Rebooting",
                'parents': ['SysKernel']
            },
            
            'panic_on_oops': {
                'desc': "Controls the kernel's behaviour when an oops or BUG is encountered",
                'label': "Panic On Oops/Bugs",
                'parents': ['SysKernel']
            },
            
            'panic_on_unrecovered_nmi': {
                'desc': "SysKernel behaviour in case of unrecovered NMI. The default Linux behaviour on an NMI of either memory or unknown is to continue operation. For many environments such as scientific computing it is preferable that the box is taken out and the error dealt with than an uncorrected parity/ECC error get propagated",
                'label': "Panic On Unrecovered NMI",
                'parents': ['SysKernel']
            },
            
            'pid_max': {
                'desc': "PID allocation wrap value. When the kernel's next PID value reaches this value, it wraps back to a minimum PID value. PIDs of value pid_max or larger are not allocated. The default is 32768",
                'label': "Maximum PID Value",
                'parents': ['SysKernel']
            },
            
            'poweroff_cmd': {
                'desc': "The command defined in this sysctl is called by various pieces of code around the kernel that want to be able to trigger an orderly poweroff. If the orderly poweroff fails, kernel will force an immediate shutdown",
                'label': "Power OFF Command",
                'parents': ['SysKernel']
            },
            
            'print-fatal-signals': {
                'desc': "Enables printing of some minimal information about userspace segfaults to the kernel console. This is useful to find early bootup bugs where userspace debugging is very hard. Defaults to off",
                'label': "Print Fatal Signals",
                'parents': ['SysKernel']
            },
            
            'printk': {
                'desc': "Influences printk() behavior when printing or logging error messages",
                'label': "Printk() Behaviour",
                'parents': ['SysKernel']
            },
            
            'printk_ratelimit': {
                'desc': "Specifies the minimum length of time between these messages (in seconds), by default we allow one every 5 seconds. A value of 0 will disable rate limiting",
                'label': "Printk Rate Limit",
                'parents': ['SysKernel']
            },
            
            'printk_ratelimit_burst': {
                'desc': "Specifies the number of messages we can send before ratelimiting kicks in",
                'label': "Printk Rate Limit Burst",
                'parents': ['SysKernel']
            },
            
            'max': {
                'desc': "Defines the maximum number of Unix 98 pseudo-terminals",
                'label': "Maximum Number of Unix 98",
                'parents': ['SysKernel']
            },
            
            'nr': {
                'desc': "Indicates how many Unix 98 pseudo-terminals are currently in use",
                'label': "Number of Unix 98 in Use",
                'parents': ['SysKernel']
            },
            
            'boot_id': {
                'desc': "Contains random string like 6fd5a44b-35f4-4ad4-a9b9-6b9be13e1fe9. This one was generated once at boot",
                'label': "Random Boot String",
                'parents': ['SysKernel']
            },
            
            'entropy_avail': {
                'desc': "Gives the available entropy. Normally, this will be 4096 (bits), a full entropy pool",
                'label': "Available Entropy",
                'parents': ['SysKernel']
            },
            
            'poolsize': {
                'desc': "Gives the size of the entropy pool. Normally, this will be 4096 bits (512 bytes). It can be changed to any value for which an algorithm is available. Currently the choices are: 32, 64, 128, 256, 512, 1024, 2048",
                'label': "Entropy Pool Size",
                'parents': ['SysKernel']
            },
            
            'read_wakeup_threshold': {
                'desc': "Contains the number of bits of entropy required for waking up processes that sleep waiting for entropy from /dev/random. The default is 64",
                'label': "Read Wakeup Threshold",
                'parents': ['SysKernel']
            },
            
            'uuid': {
                'desc': "Contains random string like 6fd5a44b-35f4-4ad4-a9b9-6b9be13e1fe9. This one is generated afresh for each read",
                'label': "Random After-Read String",
                'parents': ['SysKernel']
            },
            
            'write_wakeup_threshold': {
                'desc': "Contains the number of bits of entropy below which we wake up processes that do a select() or poll() for write access to /dev/random",
                'label': "Write WakeUp Threshold",
                'parents': ['SysKernel']
            },
            
            'randomize_va_space': {
                'desc': "Address space randomization (security feature) if enabled (1), which is the default",
                'label': "Address Space Randomization",
                'parents': ['SysKernel']
            },
            
            'real-root-dev': {
                'desc': "Exists if there is initrd support compiled in the kernel. In that case, the real root device can be changed from within linuxrc by writing the number of the new root filesystem device to this file",
                'label': "Real Root Device",
                'parents': ['SysKernel']
            },
            
            'sched_compat_yield': {
                'desc': "Makes sys_sched_yield() be more aggressive, by moving the yielding task to the last position in the rbtree. The default is 0 (what Ingo Molnar likes)",
                'label': "",
                'parents': ['SysKernel']
            },
            
            'sem': {
                'desc': "Contains 4 numbers defining limits for System V IPC semaphores. SEMMSL - the maximum number of semaphores per semaphore set. SEMMNS - a system-wide limit on the number of semaphores in all semaphore sets. SEMOPM - the maximum number of operations that may be specified in a semop(2) call. SEMMNI - a system-wide limit on the maximum number of semaphore identifiers",
                'label': "",
                'parents': ['SysKernel']
            },
            
            'sg-big-buff': {
                'desc': "Shows the size of the generic SCSI device (sg) buffer. Not tunable yet, but could be changed on compile time by editing include/scsi/sg.h and changing the value of SG_BIG_BUFF. However, there shouldn't be any reason to change this value",
                'label': "Size of SCSI Device Buffer",
                'parents': ['SysKernel']
            },
            
            'shmall': {
                'desc': "Contains the system-wide limit on the total number of pages of System V IPC shared memory. The default value is 2097152",
                'label': "Total Number of Pages of Shared Memory",
                'parents': ['SysKernel']
            },
            
            'shmmax': {
                'desc': "Sets the run time limit on the maximum System V IPC shared memory segment size that can be created. Shared memory segments up to 1GB are now supported in the kernel. This value defaults to 33554432 (32MB",
                'label': "RunTime Limit for Maximum Memory Segment Size",
                'parents': ['SysKernel']
            },
            
            'shmmni': {
                'desc': "Specifies the system-wide maximum number of System V IPC shared memory segments that can be created. The default value is 4096",
                'label': "SystemWide Maximum Number of Shared Memory Segments",
                'parents': ['SysKernel']
            },
            
            'max-threads': {
                'desc': "The maximum number of threads that should in the slow work pool. May be anywhere between min-threads and 255 or NR_CPUS * 2, whichever is greater",
                'label': "Maximum Number of Threads in Slow Work Pool",
                'parents': ['SysKernel']
            },
            
            'min-threads': {
                'desc': "The minimum number of threads that should be in the slow work pool whilst it is in use. This may be anywhere between 2 and max-threads",
                'label': "Minimum Number of Threads in Slow Work Pool",
                'parents': ['SysKernel']
            },
            
            'vslow-percentage': {
                'desc': "The percentage of active threads in the slow work pool that may be used to execute very slow work items. This may be between 1 and 99. The resultant number is bounded to between 1 and one fewer than the number of active threads. This ensures there is always at least one thread that can process very slow work items, and always at least one thread that will not",
                'label': "Active Threads in Slow Work Pool Percentage",
                'parents': ['SysKernel']
            },
            
            'sysrq': {
                'desc': "Controls the functions allowed to be invoked via the SysRq key. By default the file contains 1 which means that every possible SysRq request is allowed",
                'label': "SesRq Functions Control",
                'parents': ['SysKernel']
            },
            
            'tainted': {
                'desc': "Specifies whether the kernel has been tainted. Non-zero if the kernel has been tainted",
                'label': "Is SysKernel Tainted",
                'parents': ['SysKernel']
            },
            
            'threads-max': {
                'desc': "Specifies the limit on the maximum number of running threads system-wide",
                'label': "Maximum Number of Running Threads",
                'parents': ['SysKernel']
            },
            
            'unknown_nmi_panic': {
                'desc': "Affects behavior of handling NMI (Non-Maskable Interrupt). When the value is non-zero, unknown NMI is trapped and then panic occurs. At that time, kernel debugging information is displayed on console. That can ease the process of diagnosing system hangs",
                'label': "Unknown NMI Panic",
                'parents': ['SysKernel']
            },
            
            'userprocess_debug': {
                'desc': "Enables user process debugging",
                'label': "User Process Debugging",
                'parents': ['SysKernel']
            },
                        
            'version': {
                'desc': "Indicates the version of the kernel",
                'label': "SysKernel Version",
                'parents': ['SysKernel']
            },
 
        }

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

        tree, _, _ = traverse_directory(SysKernel.KERNEL, verbose=verbose)
        return tree


if __name__ == "__main__":
    k = SysKernel()
    k.test_parse()
