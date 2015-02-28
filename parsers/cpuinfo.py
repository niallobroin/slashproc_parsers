#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser


class CpuInfo(BasicSPParser):

    CPUINFO = "/proc/cpuinfo"

    def __init__(self):
        super(CpuInfo, self).__init__(self)


    @staticmethod
    def get_groups():
        """
        Enumerate the groups depending on the number of cores
        :rtype dict
        """
        retdict = CpuInfo.parse_cpuinfo()
        groups = {'core': {'name': 'cpuinfo', 'parents': ['root']}}

        for i in retdict['core']:
            groups[CpuInfo.key_format(i)] = {'name': i, 'parents': ['core']}

        return groups

    @staticmethod
    def get_vars():
        """
        Create the vars from the first core entry.
        Assumes all the cores are the same!!
        :rtype dict
        """
        retdict = CpuInfo.parse_cpuinfo()
        thevars = dict()
        parents = retdict['core'].keys()
       
        
        for i in retdict['core']['core0']:
            thevars[CpuInfo.key_format(i)] = {'name': i,
                                              'unit': '',
                                              'parents': parents}


        # TODO Add desc to every entry here 
        thevars['processor']['desc'] = "Provides each processor with an identifying number. On systems that have one processor, only a 0 is present."
        thevars['cpu_family']['desc'] =  "Authoritatively identifies the type of processor in the system. For an Intel-based system, place the number in front of '86' to determine the value. This is particularly helpful for those attempting to identify the architecture of an older system such as a 586, 486, or 386. Because some RPM packages are compiled for each of these particular architectures, this value also helps users determine which packages to install."
        thevars['model_name']['desc'] = "Displays the common name of the processor, including its project name."
        thevars['cpu_mhz']['desc'] = "Shows the precise speed in megahertz for the processor to the thousandths decimal place."
        thevars['cpu_mhz']['unit'] = 'MHz'
        thevars['cache_size']['desc'] = "Displays the amount of level 2 memory cache available to the processor."
        thevars['cache_size']['unit'] = 'KB'
        thevars['siblings']['desc'] = "Displays the number of sibling CPUs on the same physical CPU for architectures which use hyper-threading."
        thevars['flags']['desc'] = "Defines a number of different qualities about the processor, such as the presence of a floating point unit (FPU) and the ability to process MMX instructions."





        return thevars


    @staticmethod
    def get_data():
        """
        Returns the parsed directory
        :rtype dict
        """
        return CpuInfo.parse_cpuinfo()


    @staticmethod
    def parse_cpuinfo():
        """
        Parse /proc/cpuinfo
        :rtype dict
        """
        retdict = {'core': dict()}
        for l in open(CpuInfo.CPUINFO):
            line = l.split(':')

            #processor_num = 0
            if len(line) == 2:
                k = line[0].strip().replace('\t','').replace('\n','').replace(' ', '_').lower()
                v = line[1].strip().replace('\t','').replace('\n','')
                if k == 'processor':
                    processor_num =  'core' + v
                    retdict['core'][processor_num] = dict()


                retdict['core'][processor_num][k] = v
                if k == 'cache_size':
                    retdict['core'][processor_num]['cache_size'] = v.strip()[0]

        return retdict


if __name__ == "__main__":
    c = CpuInfo()
    c.test_parse()




