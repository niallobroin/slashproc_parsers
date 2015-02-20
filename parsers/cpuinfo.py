#!/usr/bin/env python

from sp_parser.basic_sp_parser import BasicSPParser


class CpuInfo(BasicSPParser):

    CPUINFO = "/proc/cpuinfo"

    def __init__(self):
        super(CpuInfo, self).__init__(self)


    @staticmethod
    def get_groups():
        """
        Static method to define groups that that sp_parser can parse
        """
        retdict = CpuInfo.parse_cpuinfo()
        groups =  {'core': {'name': 'cpuinfo', 'parents': ['root']}}

        for i in retdict['core']:
            groups[CpuInfo.key_format(i)] = {'name': i, 'parents': ['core']}

        return groups

    @staticmethod
    def get_vars():
        """
        Static method to define vars that that sp_parser can parse
        """
        retdict = CpuInfo.parse_cpuinfo()
        thevars = dict()
        parents = retdict['core'].keys()
       
        
        for i in retdict['core']['core0']:
            thevars[CpuInfo.key_format(i)] = {'name': i,
                                              'unit': '',
                                              'parents': parents}
        
        return thevars


    @staticmethod
    def get_data():
        return CpuInfo.parse_cpuinfo()


    @staticmethod
    def parse_cpuinfo():
        """
        Parse /proc/cpuinfo
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

        return retdict


if __name__ == "__main__":
    c = CpuInfo()
    c.test_parse()




