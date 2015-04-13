#!/usr/bin/env python

from slashproc_parser.basic_parser import BasicSPParser


class CpuInfo(BasicSPParser):
    """
    Parser for /proc/cpuinfo
    """
    CPUINFO = "/proc/cpuinfo"

    def __init__(self):
        super(CpuInfo, self).__init__(self)


    @staticmethod
    def get_groups():
        """
        Enumerate the groups depending on the number of cores
        :rtype dict
        """
        groups = {'cpuinfo': {'label': 'CPU Information', 'parents': ['root']}}

        for i in CpuInfo.get_data()['cpuinfo']:
            groups[CpuInfo.key_format(i)] = {'label': i, 'parents': ['cpuinfo']}

        return groups

    @staticmethod
    def get_vars():
        """
        Create the vars from the first core entry.
        Assumes all the cores are the same!!
        :rtype dict
        """
        data = CpuInfo.get_data()
        parents = data['cpuinfo'].keys()
       
       
        thevars = {
            'processor': {
                'desc': "Provides each processor with an identifying number. On systems that have one processor, only a 0 is present",
                'label': 'Processor ID',
                'parents': ['cpuinfo']
            },
            
            'cpu_family': {
                'desc': "Authoritatively identifies the type of processor in the system. For an Intel-based system, place the number in front of '86' to determine the value. This is particularly helpful for those attempting to identify the architecture of an older system such as a 586, 486, or 386. Because some RPM packages are compiled for each of these particular architectures, this value also helps users determine which packages to install",
                'label': 'Type of the CPU',
                'parents': ['cpuinfo']
            },
            
            'model_label': {
                'desc': "Displays the common label of the processor, including its project label",
                'label': 'Common Label of the CPU',
                'parents': ['cpuinfo']
            },
            
            'cpu_mhz': {
                'desc': "Shows the precise speed in megahertz for the processor to the thousandths decimal place",
                'label': 'CPU Speed in Mhz',
                'parents': ['cpuinfo']
            },
            
            'cache_size': {
                'desc': "Displays the amount of level 2 memory cache available to the processor in KB",
                'label': 'Cache Size',
                'parents': ['cpuinfo']
            },
            
            'siblings': {
                'desc': "Displays the number of sibling CPUs on the same physical CPU for architectures which use hyper-threading",
                'label': 'Number of Sibling CPU',
                'parents': ['cpuinfo']
            },
            
            'flags': {
                'desc': "Defines a number of different qualities about the processor, such as the presence of a floating point unit (FPU) and the ability to process MMX instructions",
                'label': 'CPU flags',
                'parents': ['cpuinfo']
            },
            
            'acpi': {
                'desc': "Supports the Advanced Configuration and Power Interface",
                'label': 'Advanced Configuration and Power Interface',
                'parents': ['cpuinfo']
            },
            
            'aes': {
                'desc': "Support of instruction set that improves performance of AES encoding/decoding ",
                'label': 'AES Performance Improvement',
                'parents': ['cpuinfo']
            },
            
            'aperfmperf': {
                'desc': "Supports MSR  APERF/MPERF registers for determining the current operating frequency for each core processor",
                'label': 'MSR APERF/ MPERF Registers',
                'parents': ['cpuinfo']
            },
            
            'apic': {
                'desc': "Supports Advanced Programmable Interrupt Controller",
                'label': 'Advanced Programmable Interrupt Controller',
                'parents': ['cpuinfo']
            },
            
            'arat': {
                'desc': "Continuous operation of APIC timer even in the case when the kernel goes into power saving mode (C-state)",
                'label': 'Always Running APIC timer',
                'parents': ['cpuinfo']
            },
            
            'avx': {
                'desc': "Supports a variety of improvements, new regulations and new encoding schemes of machine code",
                'label': 'Advanced Vector Extensions',
                'parents': ['cpuinfo']
            },
            
            'bts': {
                'desc': "Supports bit testing instruction set",
                'label': 'Bit Test',
                'parents': ['cpuinfo']
            },
            
            'clflush': {
                'desc': "Supports cache data processing instructions",
                'label': 'Cache Line Flush',
                'parents': ['cpuinfo']
            },
            
            'cmov': {
                'desc': "Supports additional instuction set: Conditional move and compare instructions",
                'label': 'Conditional Move and Compare Instructions',
                'parents': ['cpuinfo']
            },
            
            'constant_tsc': {
                'desc': "TSC has a constant frequency, it allows TSC determine the maximum frequency of the processor regardless of its current",
                'label': 'TSC determined CPU Frequency',
                'parents': ['cpuinfo']
            },
            
            'arch_perfmon': {
                'desc': "Supports performance monitoring subsystem",
                'label': 'Performance Monitoring',
                'parents': ['cpuinfo']
            },
            
            'cx8': {
                'desc': "Supports CMPXCHG8B instruction",
                'label': 'CMPXCHG8B',
                'parents': ['cpuinfo']
            },
            
            'cx16': {
                'desc': "Supports CMPXCHG16B instruction for multiprocessor calculations",
                'label': 'CMPXCHG16B',
                'parents': ['cpuinfo']
            },
            
            'dca': {
                'desc': "Supports carrying out preliminary sampling of the devices displayed in the memory (memory-mapped)",
                'label': 'Direct Cache Access',
                'parents': ['cpuinfo']
            },
            
            'de': {
                'desc': "Supports debug extensions instructions",
                'label': 'Debug Extensions',
                'parents': ['cpuinfo']
            },
            
            'ds_cpl': {
                'desc': "Supports additional options for storing debugging information",
                'label': 'CPL Qualified Debug Store',
                'parents': ['cpuinfo']
            },
            
            'dtes64': {
                'desc': "Supports 64-bit debug store",
                'label': '64-Bit Debug Store',
                'parents': ['cpuinfo']
            },
            
            'dts': {
                'desc': "Supports digital thermal sensor",
                'label': 'Digital Thermal Sensor',
                'parents': ['cpuinfo']
            },
            
            'epb': {
                'desc': "Supports energy efficiency options available through MSR",
                'label': 'Energy Performance Bias',
                'parents': ['cpuinfo']
            },
            
            'ept': {
                'desc': "Supports memory pages translation in the virtual environment",
                'label': 'Extended Page Table',
                'parents': ['cpuinfo']
            },
            
            'est': {
                'desc': "Supports power-saving mode based on the dynamic changes in the frequency and power consumption of the processor",
                'label': 'Enhanced Intel Speedstep',
                'parents': ['cpuinfo']
            },
            
            'flexpriority': {
                'desc': "Supports access to the registers of the TPR virtual environments. Reduces the number of context switches when accessing the APIC",
                'label': 'Flexible Priority',
                'parents': ['cpuinfo']
            },
            
            'fpu': {
                'desc': "Has floating point unit block that performs most of the mathematical calculations",
                'label': 'Floating Point Unit',
                'parents': ['cpuinfo']
            },
            
            'fxsr': {
                'desc': "Support FXSAVE/FXRSTOR instructions used for fast context switching",
                'label': 'FXSAVE/FXRSTOR Instructions',
                'parents': ['cpuinfo']
            },
            
            'ht': {
                'desc': "Hyper-Transport (AMD CPUs) or Hyper-Threading (Intel CPU)",
                'label': 'Hyper-Transport/ Hyper-Threading',
                'parents': ['cpuinfo']
            },
            
            'htt': {
                'desc': "The possibility of using a single physical processor as two logical CPUs",
                'label': 'Hyper-Threading Technology',
                'parents': ['cpuinfo']
            },
            
            'ida': {
                'desc': "Supports increasing of the frequency of the processor that runs in a single-threaded mode",
                'label': 'Intel Dynamic Acceleration',
                'parents': ['cpuinfo']
            },
            
            'lahf_lm': {
                'desc': "Supports LAHF/SAHF in a 64-bit mode",
                'label': 'LAHF/SAHF Instructions',
                'parents': ['cpuinfo']
            },
            
            'lm': {
                'desc': "Supports 64-bit mode",
                'label': 'Long Mode',
                'parents': ['cpuinfo']
            },
            
            'mca': {
                'desc': "Supports OS notification mechanism of hardware errors detected by the processor",
                'label': 'Machine Check Architecture',
                'parents': ['cpuinfo']
            },
            
            'mce': {
                'desc': "Supports hardware exceptions verification caused by processor hardware errors",
                'label': 'Machine Check Exception',
                'parents': ['cpuinfo']
            },
            
            'mmx': {
                'desc': "Supports multimedia procession instruction set",
                'label': 'MultiMedia eXtension',
                'parents': ['cpuinfo']
            },
            
            'monitor': {
                'desc': "Supports MONITOR/MWAIT instructions",
                'label': 'CPU Monitor',
                'parents': ['cpuinfo']
            },
            
            'msr': {
                'desc': "Supports performance monitoring, debugging and tracing registers that provides CPU service information",
                'label': 'Model Specific Registers',
                'parents': ['cpuinfo']
            },
            
            'mtrr': {
                'desc': "Supports additional instructions set that provides information about the range of memory cached by processor",
                'label': 'Memory Type Range Register',
                'parents': ['cpuinfo']
            },
            
            'nonstop_tsc': {
                'desc': "Supports NONSTOP_TSC bit that works in conjunction with CONSTANT_TSC",
                'label': 'NONSTOP_TSC bit',
                'parents': ['cpuinfo']
            },
            
            'nopl': {
                'desc': "Supports No Operation Instruction",
                'label': 'No Operation, Long',
                'parents': ['cpuinfo']
            },
            
            'nx': {
                'desc': "Supports no execute instructions",
                'label': 'No Execute',
                'parents': ['cpuinfo']
            },
            
            'pae': {
                'desc': "Allows working with a physical memory that has a size that is larger than 4GB",
                'label': 'Physical Address Extensions',
                'parents': ['cpuinfo']
            },
            
            'pat': {
                'desc': "Provides information about the cached memory areas",
                'label': 'Page Attribute Table',
                'parents': ['cpuinfo']
            },
            
            'pbe': {
                'desc': "Supports the use of FERR # / PBE # instructions to return to the normal operating mode for the interrupt handler",
                'label': 'Pending Break Encoding',
                'parents': ['cpuinfo']
            },
            
            'pcid': {
                'desc': "Supports Association of TLB-identifiers with specific processes",
                'label': 'Process Context Identifiers',
                'parents': ['cpuinfo']
            },
            
            'pclmulqdq': {
                'desc': "Supports PCLMULQDQ instruction that is used in cryptography",
                'label': 'PCLMULQDQ Instruction',
                'parents': ['cpuinfo']
            },
            
            'pdcm': {
                'desc': "Support additional MSR registers responsible for performance",
                'label': 'Perfmon and Debug Capability',
                'parents': ['cpuinfo']
            },
            
            'pdpe1gb': {
                'desc': "Supports 1Gb pages (HugePages)",
                'label': 'HugePages',
                'parents': ['cpuinfo']
            },
            
            'pebs': {
                'desc': "Supports additional monitoring capabilities that allow collection of low-level statistics for the processor",
                'label': 'Precise Event Based Sampling',
                'parents': ['cpuinfo']
            },
            
            'pge': {
                'desc': "Supports tagging of TLB-entries that are common to different tasks and do not require cleaning",
                'label': 'PTE Global Bit',
                'parents': ['cpuinfo']
            },
            
            'pln': {
                'desc': "Supports event notification while the processor switches between performance states (P-state)",
                'label': 'Power Limit Notification',
                'parents': ['cpuinfo']
            },
            
            'pni': {
                'desc': "Supports SSE3 instruction set",
                'label': 'Prescott New Instruction',
                'parents': ['cpuinfo']
            },
            
            'popcnt': {
                'desc': "Supports POPCNT instruction",
                'label': 'POPCNT Instruction',
                'parents': ['cpuinfo']
            },
            
            'pse': {
                'desc': "Supports mode that allows processors to use pages bigger than standard page size (4KB)",
                'label': 'Page Size Extensions',
                'parents': ['cpuinfo']
            },
            
            'pse36': {
                'desc': "Supports expansion of the PSE that can address up to 64 gigabytes of RAM not activating PAE",
                'label': 'Page Size Extensions 36',
                'parents': ['cpuinfo']
            },
            
            'pts': {
                'desc': "Supports the ability to display the output of the temperature sensor",
                'label': 'Package Thermal Status',
                'parents': ['cpuinfo']
            },
            
            'rdtscp': {
                'desc': "Supports service manual for working with TSC",
                'label': 'TSC Service Manual',
                'parents': ['cpuinfo']
            },
            
            'rep_good': {
                'desc': "Supports pseudo-flag appointed by the kernel",
                'label': 'Pseudo-Flag',
                'parents': ['cpuinfo']
            },
            
            'sep': {
                'desc': "Supports SYSENTER and SYSEXIT instructions for fast control transfer to OS",
                'label': 'SYSENTER/SYSEXIT Instructions',
                'parents': ['cpuinfo']
            },
            
            'smx': {
                'desc': "Supports TXT mode (Trusted Execution Technology)",
                'label': 'Safer Mode Extensions',
                'parents': ['cpuinfo']
            },
            
            'ss': {
                'desc': "Allows processor to resolve conflicts in its own memory",
                'label': 'Self Snoop',
                'parents': ['cpuinfo']
            },
            
            'sse': {
                'desc': "Supports additional various instruction set (SIMD extensions)",
                'label': 'Streaming SIMD Extensions',
                'parents': ['cpuinfo']
            },
            
            'sse2': {
                'desc': "Supports additional various instruction set (SIMD extensions 2)",
                'label': 'Streaming SIMD Extensions 2',
                'parents': ['cpuinfo']
            },
            
            'sse3': {
                'desc': "Supports additional various instruction set (SIMD extensions 3)",
                'label': 'Streaming SIMD Extensions 3',
                'parents': ['cpuinfo']
            },
            
            'ssse3': {
                'desc': "Supports additional instructions for the SSE3 set (SIMD extensions 3)",
                'label': 'Supplemental SSE3',
                'parents': ['cpuinfo']
            },
            
            'sse4': {
                'desc': "Supports additional various instruction set (SIMD extensions 4)",
                'label': 'Streaming SIMD Extensions 4',
                'parents': ['cpuinfo']
            },
            
            'sse4_1': {
                'desc': "Supports additional instruction set for the SSE4 set (SIMD extensions 4)",
                'label': 'SSE4 Extension 1',
                'parents': ['cpuinfo']
            },
            
            'sse4_2': {
                'desc': "Supports additional instruction set for the SSE4 set (SIMD extensions 4)",
                'label': 'SSE4 Extension 2',
                'parents': ['cpuinfo']
            },
            
            'syscall': {
                'desc': "Supports mechanism used by applications to request services from the operating system kernel",
                'label': 'System Call',
                'parents': ['cpuinfo']
            },
            
            'tm': {
                'desc': "Supports anti-overheating module",
                'label': 'Thermal Monitor',
                'parents': ['cpuinfo']
            },
            
            'tm2': {
                'desc': "Supports anti-overheating module extension 2",
                'label': 'Thermal Monitor Extension 2',
                'parents': ['cpuinfo']
            },
            
            'tpr_shadow': {
                'desc': "Supports functions that reduce the number of calls initiated by the hypervisor when accessing the TPR",
                'label': 'TPR Shadow',
                'parents': ['cpuinfo']
            },
            
            'tsc': {
                'desc': "Supports CPU time stamp counter",
                'label': 'Time Stamp Counter',
                'parents': ['cpuinfo']
            },
            
            'tsc_deadline_timer': {
                'desc': "Supports high-precision mode for TSC deadline timer",
                'label': 'TSC High Precision Mode',
                'parents': ['cpuinfo']
            },
            
            'vnmi': {
                'desc': "Supports extended processing of some types of interruptions",
                'label': 'NMI-window exiting',
                'parents': ['cpuinfo']
            },
            
            'vme': {
                'desc': "Supports extended instructions for 8086 mode",
                'label': '8086 Mode Instructions',
                'parents': ['cpuinfo']
            },
            
            'vmx': {
                'desc': "Supports virtual machine extensions",
                'label': 'Virtual Machine Extensions',
                'parents': ['cpuinfo']
            },
            
            'vpid': {
                'desc': "Supports virtual-processors identifiers",
                'label': 'Virtual-Processor Identifiers',
                'parents': ['cpuinfo']
            },
            
            'xsave': {
                'desc': "Supports XSAVE/XRSTOR instructions",
                'label': 'XSAVE/XRSTOR instructions',
                'parents': ['cpuinfo']
            },
            
            'xsaveopt': {
                'desc': "Supports XSAVE instruction improvement that reduces the amount of data to be recorded as a result of XSAVE",
                'label': 'XSAVE Extension',
                'parents': ['cpuinfo']
            },
            
            'xtopology': {
                'desc': "Supports improved ability to work with a list of CPUID topology",
                'label': 'CPUID Topology',
                'parents': ['cpuinfo']
            },
            
            'xtpr': {
                'desc': "Supports disabling of sending Task Priority Messages",
                'label': 'xTPR Update Control',
                'parents': ['cpuinfo']
            },


        }


        #TODO Cheat for the rest of thevars
        for i in data['cpuinfo']['core0']:
            if i not in thevars:
                thevars[CpuInfo.key_format(i)] = {'label': i,
                                                  'parents': parents}
            else:
                thevars[i]['parents'] = parents

        return thevars


    @staticmethod
    def get_data():
        """
        Parse /proc/cpuinfo
        :rtype dict
        """
        def clean_key(txt):
            txt.strip().lower()
            return txt.replace('\t', '').replace('\n', '').replace(' ', '_')

        data = dict()
        for l in open(CpuInfo.CPUINFO):
            line = l.split(':')

            #processor_num = 0
            if len(line) == 2:
                k = clean_key(line[0])
                v = line[1].strip().replace('\t', '').replace('\n', '')
                if k == 'processor':
                    processor_num = 'core' + v
                    data[processor_num] = dict()

                data[processor_num][k] = v
                if k == 'cache_size':
                    data[processor_num]['cache_size'] = v.strip()[0]

        return {'cpuinfo': data}


if __name__ == "__main__":
    c = CpuInfo()
    c.test_parse()




