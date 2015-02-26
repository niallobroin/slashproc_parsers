#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser


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

            'processor': {'desc': "Provides each processor with an identifying number. On systems that have one processor, only a 0 is present."},

            'cpu_family': {'desc': "Authoritatively identifies the type of processor in the system. For an Intel-based system, place the number in front of '86' to determine the value. This is particularly helpful for those attempting to identify the architecture of an older system such as a 586, 486, or 386. Because some RPM packages are compiled for each of these particular architectures, this value also helps users determine which packages to install."},

            'model_label': {'desc': "Displays the common label of the processor, including its project label."},

            'cpu_mhz': {'desc': "Shows the precise speed in megahertz for the processor to the thousandths decimal place.",
                        'unit': 'MHz'},

            'cache_size': {'desc': "Displays the amount of level 2 memory cache available to the processor.",
                           'unit': 'KB'},

            'siblings': {'desc': "Displays the number of sibling CPUs on the same physical CPU for architectures which use hyper-threading."},

            'flags': {'desc': "Defines a number of different qualities about the processor, such as the presence of a floating point unit (FPU) and the ability to process MMX instructions."},

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




