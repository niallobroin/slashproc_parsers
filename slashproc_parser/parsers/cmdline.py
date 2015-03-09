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

            'cachesize': {
                'desc': 'Overrides level 2 CPU cache size detection. Measured in units of bytes',
                'label': "Cache Size",
                'parents': ['cmdline']
            },

            'lpj': {
                'desc': 'Specifies the loops per jiffy that should be used by the kernel to avoid the time-consuming boot-time autodetection',
                'label': "Loops Per Jiffy",
                'parents': ['cmdline']
            },
            
            'nmi_watchdog': {
                'desc': 'Allows the user to override the default non-maskable interrupt (NMI) watchdog value',
                'label': "NMI Watchdog",
                'parents': ['cmdline']
            },
            
            'no387': {
                'desc': 'Always use the 387 math emulation library, even if a 387 math coprocessor is present in the system',
                'label': "387 Emulation Library",
                'parents': ['cmdline']
            },
            
            'nofxsr': {
                'desc': 'Disable the x86 floating-point extended register save and restore. The kernel will save only legacy floating-point registers on a task switch',
                'label': "No x86 Register",
                'parents': ['cmdline']
            },
            
            'no-hlt': {
                'desc': 'Tells the kernel not to use the HLT instruction',
                'label': "No HLT Instruction",
                'parents': ['cmdline']
            },
            
            'mce': {
                'desc': 'Turns the machine check exception subsystem on, if it has been built into the kernel configuration',
                'label': "Machine Check Exception",
                'parents': ['cmdline']
            },
            
            'nomce': {
                'desc': 'Disables the machine check exception feature',
                'label': "No Machine Check Exception",
                'parents': ['cmdline']
            },
            
            'nosep': {
                'desc': 'Disables x86 SYSENTER/SYSEXIT support in the kernel. This can cause some system calls to take longer',
                'label': "No x86 SYSENTER/SYSEXIT",
                'parents': ['cmdline']
            },
            
            'nosmp': {
                'desc': 'Tells an SMP kernel to act as a uniprocessor kernel, even on a multiprocessor machine',
                'label': "No MultiProcessor",
                'parents': ['cmdline']
            },
            
            'notsc': {
                'desc': 'Disables the time stamp counter hardware in the system, if present',
                'label': "No TimeStamp Counter",
                'parents': ['cmdline']
            },
            
            'max_cpus': {
                'desc': 'Specifies the maximum number of processors that a SMP kernel should use, even if there are more processors present in the system',
                'label': "Maximum CPUs",
                'parents': ['cmdline']
            },
            
            'isolcpus': {
                'desc': 'Removes the specified CPUs, as defined by the cpu_number values, from the general kernel SMP balancing and scheduler algroithms',
                'label': "Isolate CPUs ",
                'parents': ['cmdline']
            },
            
            'migration_cost': {
                'desc': 'Debugging option that overrides the default scheduler migration cost matrix',
                'label': "Override Migration Cost",
                'parents': ['cmdline']
            },
            
            'migration_debug': {
                'desc': 'Sets the migration cost debug level. 0 : no extra messages will be printed to the kernel log. 1 : some information on how the matrix is determined. 2 : very verbose and is useful only with a serial console',
                'label': "Migration Cost Debug Level",
                'parents': ['cmdline']
            },
            
            'migration_factor': {
                'desc': 'Modifies the default migration costs by the specified percentage. The debugging option can be used to proportionally increase or decrease the auto-detected migration costs for all entries of the migration matrix',
                'label': "Migration Factor",
                'parents': ['cmdline']
            },
            
            'initrd': {
                'desc': 'Specifies where the initial ramdisk for the kernel boot is located',
                'label': "Initial RamDisk Location",
                'parents': ['cmdline']
            },
            
            'load_ramdisk': {
                'desc': 'A ramdisk is loaded by the kernel at boot time from the floppy drive',
                'label': "Load RamDisk",
                'parents': ['cmdline']
            },
            
            'noinitrd': {
                'desc': 'Do not load any initial ramdisk, even if it is configured in other options passed to the kernel',
                'label': "No RamDisk Load",
                'parents': ['cmdline']
            },
            
            'prompt_ramdisk': {
                'desc': 'Prompts the user for the initial ramdisk before attempting to read it from the floppy drive',
                'label': "Prompt RamDisk List",
                'parents': ['cmdline']
            },
            
            'ramdisk_blocksize': {
                'desc': 'Tells the ramdisk driver how many bytes to use per block. The default size is 1024',
                'label': "RamDisk BlockSize",
                'parents': ['cmdline']
            },
            
            'ramdisk_size': {
                'desc': 'Specifies the size of the initial RAM disk in kilobytes. The default size is 4096 (4 MB)',
                'label': "RamDisk Size",
                'parents': ['cmdline']
            },
            
            'rootdelay': {
                'desc': 'Wait n seconds before trying to mount the root filesystem. Useful if the root filesystem is on a USB or Firewire device',
                'label': "Root Delay",
                'parents': ['cmdline']
            },
            
            'rootflags': {
                'desc': 'The root filesystem mount options',
                'label': "Root Flags",
                'parents': ['cmdline']
            },
            
            'rootfstype': {
                'desc': 'Tries to mount the root filesystem as this type of filesystem',
                'label': "Root FileSystem Type",
                'parents': ['cmdline']
            },
            
            'rw': {
                'desc': 'Mounts the root device as read-write on boot',
                'label': "Mount as Read-Write",
                'parents': ['cmdline']
            },
            
            'init': {
                'desc': 'Runs the specified binary as the init process instead of the default /sbin/init program',
                'label': "Initial Program",
                'parents': ['cmdline']
            },
            
            'rdinit': {
                'desc': 'Runs the program specified by full_path_name as the init process. This file must be on the kernel ramdisk instead of on the root filesystem',
                'label': "Initial Process",
                'parents': ['cmdline']
            },
            
            'S': {
                'desc': 'Runs init in single-user mode on boot',
                'label': "Single-User Mode Init",
                'parents': ['cmdline']
            },
      
            'crashkernel': {
                'desc': 'Reserves a portion of physical memory for kexec to use',
                'label': "Reserve Memory for kexec",
                'parents': ['cmdline']
            },
            
            'elfcorehdr': {
                'desc': 'Specifies the physical address where the ELF header of kernel core image starts. This is used by kexec to find the kernel when booting the secondary kernel image',
                'label': "ELF Core Header",
                'parents': ['cmdline']
            },
            
            'rcu.blimit': {
                'desc': 'Sets the maximum number of finished RCU callbacks to process in one batch',
                'label': "RCU Batch Limit",
                'parents': ['cmdline']
            },
            
            'rcu.qhimark': {
                'desc': 'Batch limiting is disabled when the number of queued RCU callbacks rises above the specified value',
                'label': "RCU Queue High Level",
                'parents': ['cmdline']
            },
            
            'rcu.qlowmark': {
                'desc': 'Batch limiting is re-enabled when the number of queued RCU callbacks falls below the specified value',
                'label': "RCU Queue Low Level",
                'parents': ['cmdline']
            },
            
            'rcu.rsinterval': {
                'desc': 'Sets the number of additional RCU callbacks that should bee queued before forcing a reschedule on all CPUs',
                'label': "RCU Callback Queue Length",
                'parents': ['cmdline']
            },
            
            'acpi': {
                'desc': 'Specifies the main option for the Advanced Configuration and Power Interface (ACPI)',
                'label': "ACPI Options",
                'parents': ['cmdline']
            },
            
            'acpi_sleep': {
                'desc': 'Sets the ACPI sleep options. ',
                'label': "ACPI Sleep Options",
                'parents': ['cmdline']
            },
            
            'acpi_sci': {
                'desc': 'Sets the ACPI System Control Interrupt trigger mode',
                'label': "ACPI in SCI Mode",
                'parents': ['cmdline']
            },
            
            'acpi_irq_balance': {
                'desc': 'Causes ACPI to balance the active IRQs. This is the default option when operating in APIC mode',
                'label': "Balance Active IRQ",
                'parents': ['cmdline']
            },
            
            'acpi_irq_nobalance': {
                'desc': 'Causes ACPI not to move the active IRQs. This is the default option when operating in PIC mode',
                'label': "No Balance of Active IRQ",
                'parents': ['cmdline']
            },
            
            'acpi_irq_isa': {
                'desc': 'If the IRQ balance option is enabled, marks the listed IRQs as used by the ISA subsystem',
                'label': "Mark IRQ Used By ISA",
                'parents': ['cmdline']
            },
            
            'acpi_irq_pci': {
                'desc': 'If the IRQ balance option is enabled, marks the listed IRQs as used by the PCI subsystem',
                'label': "Mark IRQ Used by PCI",
                'parents': ['cmdline']
            },
            
            'acpi_os_name': {
                'desc': 'Tells the ACPI BIOS the specified name of the running operating system',
                'label': "Fake OS Name",
                'parents': ['cmdline']
            },
            
            'acpi_osi': {
                'desc': 'Disables the _OSI ACPI method',
                'label': "No _OSI ACPI",
                'parents': ['cmdline']
            },
            
            'acpi_serialize': {
                'desc': 'Forces the serialization of ACPI Machine Language methods',
                'label': "Force ACPI Serialization",
                'parents': ['cmdline']
            },
            
            'acpi_skip_timer_override': {
                'desc': 'Allows the ACPI layer to recognize and ignore IRQ0/pin2 Interrupt Override issues for broken nForce2 BIOSes that result in the XT-PIC timer acting up',
                'label': "Skip Timer Override",
                'parents': ['cmdline']
            },
            
            'acpi_dbg_layer': {
                'desc': 'Sets the ACPI debug layers. The value is an integer in which each bit indicates a different ACPI debug layer. After the system has booted, the debug layers can be set via the /proc/acpi/debug_layer file',
                'label': "ACPI Debug Layer",
                'parents': ['cmdline']
            },
            
            'acpi_fake_ecdt': {
                'desc': 'If present, this allows ACPI to workaround BIOS failures when it lacks an Embedded Controller Description Table',
                'label': "ECDT workaround",
                'parents': ['cmdline']
            },
            
            'acpi_generic_hotkey': {
                'desc': 'Allows the ACPI consolidated generic hotkey driver to override the platform-specific driver if one is present',
                'label': "ACPI Generic Hotkey",
                'parents': ['cmdline']
            },
            
            'acpi_pm_good': {
                'desc': 'Forces the kernel to assume that the pmtimer of the machine latches its value and always returns good values',
                'label': "PMTimer Bug Detection",
                'parents': ['cmdline']
            },
            
            'ec_intr': {
                'desc': 'Specifies the ACPI embedded controller interrupt mode. If value is 0, polling mode will be used, otherwise interrupt mode will be used. Interrupt mode is the default',
                'label': "ACPI Interrupt Mode",
                'parents': ['cmdline']
            },
            
            'memmap': {
                'desc': 'This marks a specific location and range of memory as reserved. The value is the size of the memory location and start is the start location in memory of the range',
                'label': "Mark Memory as Reserved",
                'parents': ['cmdline']
            },
            
            'pnpacpi': {
                'desc': 'Disables the PnP ACPI functionality',
                'label': "PnP ACPI Off",
                'parents': ['cmdline']
            },
            
            'processor.max_cstate': {
                'desc': 'Limits the processor to a maximum C-state, no matter what the ACPI tables say it can support. The value is a valid C-state value. A value of 9 overrides any DMI blacklist limit that might be present for this processor',
                'label': "Maximum C-State",
                'parents': ['cmdline']
            },
            
            'processor.nocst': {
                'desc': 'Causes the ACPI core to ignore the _CST method of determining the processor C-states and use the legacy FADT method instead',
                'label': "Ignore _CST for C-State",
                'parents': ['cmdline']
            },
            
            'max_luns': {
                'desc': 'Specifies the maximum number of SCSI LUNS that the system should probe. The value is an integer from 1 to 4294967295.',
                'label': "Maximum number of SCSI LUNS",
                'parents': ['cmdline']
            },
            
            'max_report_luns': {
                'desc': 'Specifies the maximum number of SCSI LUNs that the system can receive. The value is an integer from 1 to 16384',
                'label': "Maximum number of SCSI LUNS Received",
                'parents': ['cmdline']
            },
                        
            'scsi_dev_flags': {
                'desc': 'Lets the user add entries to the SCSI black/white list for a specific vendor and model of device',
                'label': "SCSI Black/White List",
                'parents': ['cmdline']
            },
                        
            'pci': {
                'desc': 'Specifies different parameters the PCI subsystem can use',
                'label': "PCI Options",
                'parents': ['cmdline']
            },
                        
            'noisapnp': {
                'desc': 'Disables the ISA PnP subsystem, if it has been enabled in the kernel configuration',
                'label': "No ISA PnP",
                'parents': ['cmdline']
            },
                        
            'pnpbios': {
                'desc': 'Sets the main PnP BIOS settings. on enables the PnP BIOS subsystem. off disables the PnP BIOS subsystem. curr tells the PnP BIOS subsystem to use the current static settings and no-curr tells the subsystem to probe for dynamic settings if possible',
                'label': "PnP BIOS Settings",
                'parents': ['cmdline']
            },
                        
            'pnp_reserve_irq': {
                'desc': 'List of the IRQs that the PnP BIOS subsystem should not use for autoconfiguration',
                'label': "PnP BIOS Reserved IRQs",
                'parents': ['cmdline']
            },
                        
            'pnp_reserve_dma': {
                'desc': 'List of the DMAs that the PnP BIOS subsystem should not use for autoconfiguration',
                'label': "PnP BIOS Reserved DMAs",
                'parents': ['cmdline']
            },
                        
            'pnp_reserve_io': {
                'desc': 'I/O ports that the PnP BIOS subsystem should not use for autoconfiguration. Each port is listed by its starting location and size',
                'label': "PnP BIOS Reserved I/O Ports",
                'parents': ['cmdline']
            },
                        
            'pnp_reserve_mem': {
                'desc': 'Memory regions that the PnP BIOS subsystem should not use for autoconfiguration. Each region is listed by its starting location and size',
                'label': "PnP BIOS Reserved Memory Regions",
                'parents': ['cmdline']
            },
                        
            'checkreqprot': {
                'desc': 'Sets the initial checkreqprot flag value. 0 means that the check protection will be applied by the kernel and will include any implied execute protection. 1 means that the check protection is requested by the application',
                'label': "Initial CheckreqProt Flag",
                'parents': ['cmdline']
            },
                        
            'enforcing': {
                'desc': 'Specifies whether SELinux enforces its rules upon boot. 0 means that SELinux will just log policy violations but wil not deny access to anything. 1 means that the enforcement will be fully enabled with denials as well as logging',
                'label': "Initial Enforcing Status",
                'parents': ['cmdline']
            },
                        
            'selinux': {
                'desc': 'Allows SELinux to be enabled (1) or disabled (0) to boot time. The default value is set by a kernel configuration option',
                'label': "Enable SELinux",
                'parents': ['cmdline']
            },
                        
            'selinux_compat_net': {
                'desc': 'Sets the initial value for the SELinux network control model. 0 uses the new secmark-based packet controls, and 1 uses the legacy packet controls',
                'label': "SELinux Network Control",
                'parents': ['cmdline']
            },
                        
            'netdev': {
                'desc': 'Specifies network device parameters, which are specific to the driver used by the network device. Some drivers' source files document the applicable options',
                'label': "Network Device Parameters",
                'parents': ['cmdline']
            },
                        
            'rhash_entries': {
                'desc': 'Overrides the default number of hash buckets for the route cache of the kernel. Recommended only for kernel network experts',
                'label': "Route Cash Hash Buckets",
                'parents': ['cmdline']
            },
                        
            'shapers': {
                'desc': 'Sets the maximum number of network shapers that the kernel can use',
                'label': "Maximum Number of Network Shapers",
                'parents': ['cmdline']
            },
                        
            'thash_entries': {
                'desc': 'Overrides the default number of hash buckets for the kernel's TCP connection cache',
                'label': "TCP Connection Hash Buckets",
                'parents': ['cmdline']
            },
                        
            'lockd.nlm_grace_period': {
                'desc': 'Sets the NFS lock manager grace period. The value is measured in seconds',
                'label': "NFS Lock Manager Grace Period",
                'parents': ['cmdline']
            },
                        
            'lockd.nlm_tcpport': {
                'desc': 'Sets the TCP port that the NFS lock manager should use. Port must be a valid TCP port value',
                'label': "TCP Port to Lock Manager",
                'parents': ['cmdline']
            },
                        
            'lockd.nlm_timeout': {
                'desc': 'Overrides the default time value for the NFS lock manager. Value is measured in seconds. If this option is not specified the default of 10 seconds will be used',
                'label': "Lock Manager Timeout",
                'parents': ['cmdline']
            },
                        
            'lockd.nlm_udpport': {
                'desc': 'Sets the UDP port that the NFS lock manager should use. Port must be a valid UDP port value',
                'label': "UDP Port to Lock Manager",
                'parents': ['cmdline']
            },         
                        
            'nfsroot': {
                'desc': 'Specifies the NFS root filesystem.',
                'label': "NFS Root FileSystem",
                'parents': ['cmdline']
            },            
                        
            'nfs.callback_tcpport': {
                'desc': 'Specifies the TCP port that the NFSv4 callback channel should listen on. Port must be a valid TCP port value',
                'label': "NFSv4 TCP Port to Callback Channel",
                'parents': ['cmdline']
            },            
                        
            'nfs.idmap_cache_timeout': {
                'desc': 'Specifies the maximum lifetime for idmapper cache entries. The value is measured in seconds',
                'label': "Maximum Lifetime For Idmapper Cache",
                'parents': ['cmdline']
            },            
                        
            'nousb': {
                'desc': 'If this option is present, the USB subsystem will not be initialized',
                'label': "No USB",
                'parents': ['cmdline']
            },            
                        
            'lp': {
                'desc': 'Specifies the parallel port to use. The lp=port1,port2... format associates a sequence of parallel ports to devices, starting with lp0',
                'label': "Parallel Port",
                'parents': ['cmdline']
            },
                        
            'parport': {
                'desc': 'Specifies specific settings for parallel port drivers. Parallel ports are assigned in the order they are specified on the command line, starting with parport0',
                'label': "Parallel Port Parameters",
                'parents': ['cmdline']
            },
                        
            'parport_init_mode': {
                'desc': 'Specifies the mode that the parallel port should be operated in. This is necessary on the Pegasos computer where the firmware has no options for setting up the parallel port mode',
                'label': "Parallel Port Initialization Mode",
                'parents': ['cmdline']
            },
                        
            'nr_uarts': {
                'desc': 'Specifies the maximum number of different UARTs that can be registered in the kernel',
                'label': "Maximum Number of UARTs",
                'parents': ['cmdline']
            },
                        
            'enable_timer_pin_1': {
                'desc': 'Enables pin 1 of the APIC timer. This option can be useful to work around chipset bugs (on some ATI chipsets in particular)',
                'label': "Pin 1 APIC Timer",
                'parents': ['cmdline']
            },
                        
            'disable_timer_pin_1': {
                'desc': 'Disables pin 1 of the APIC timer. Useful for the same reasons as enable_timer_pin_1',
                'label': "No Pin 1 APIC Timer",
                'parents': ['cmdline']
            },
                        
            'enable_8254_timer': {
                'desc': 'Enables interrupt 0 timer routing over the 8254 chip in addition to routing over the IO-APIC. The kernel tries to set a reasonable default but sometimes this option is necessary to override it',
                'label': "8254 Timer",
                'parents': ['cmdline']
            },
                        
            'disable_8254_timer': {
                'desc': 'Disables interrupt 0 timer routing over the 8254 chip in addition to routing over the IO-APIC. The kernel tries to set a reasonable default but sometimes this option is necessary to override it',
                'label': "No 8254 Timer",
                'parents': ['cmdline']
            },
                        
            'hpet': {
                'desc': 'Disables the HPET timer source and tell the kernel to use the PIT timer source instead',
                'label': "No HPET",
                'parents': ['cmdline']
            },
                        
            'clocksource': {
                'desc': 'Overrides the default kernel clocksource and use the clocksource with the specified name instead',
                'label': "Set ClockSource",
                'parents': ['cmdline']
            },
                        
            'dhash_entries': {
                'desc': 'Overrides the default number of hash buckets for the dentry cache of the kernel',
                'label': "Number of Dentry Hash Buckets",
                'parents': ['cmdline']
            },
                        
            'elevator': {
                'desc': 'Specifies the I/O scheduler. IOSCHED_NOOP has a list of the different I/O schedulers available',
                'label': "I/O Scheduler",
                'parents': ['cmdline']
            },
                        
            'hashdist': {
                'desc': 'Distributes large hashes across NUMA nodes',
                'label': "Distribute Large Hashes",
                'parents': ['cmdline']
            },
                        
            'combined_mode': {
                'desc': 'Controls which driver uses the IDE ports in combined mode: the legacy IDE driver, libata, or both',
                'label': "IDE Driver Usage",
                'parents': ['cmdline']
            },
                        
            'max_loop': {
                'desc': 'Specifies the maximum number of loopback filesystem devices that can be mounted at the same time. The value is an integer from 1 to 256',
                'label': "Maximum Number of Loopback Devices",
                'parents': ['cmdline']
            },
                        
            'panic': {
                'desc': 'Specifies the ammount of time in seconds that the kernel should wait after a panic happens before it reboots. If this is set to 0 (the default value) the kernel will not reboot after panicking; it will simply halt',
                'label': "Time After Panic Before Reboot",
                'parents': ['cmdline']
            },
                        
            'pause_on_oops': {
                'desc': 'Tells the kernel to halt all CPUs after the first oops for n seconds before continuing',
                'label': "Delay Between Kernel Oopses",
                'parents': ['cmdline']
            },
                        
            'profile': {
                'desc': 'Affects how the kernel profiler is calculated. If schedule is specified, the schedule points are affected by the value set in number. If schedule is not specified, number is the step size as a power of two for statistical time-based profiling in the kernel',
                'label': "Kernel Profiling",
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
