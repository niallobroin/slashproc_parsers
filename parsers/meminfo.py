#!/usr/bin/env python


from basic_sp_parser import BasicSPParser



class MemInfo(BasicSPParser):

    MEMINFO = "/proc/meminfo"


    def __init__(self):
        super(MemInfo, self).__init__(self)



    @staticmethod
    def get_vars():
        """
        Static method to define vars that that parser can parse
        #Will probably be a class later.
        """
        return MemInfo.meminfo('vars')



    @staticmethod
    def get_groups():
        """
        Static method to define groups that that parser can parse
        """
        return MemInfo.meminfo('groups')



    @staticmethod
    def meminfo(param='data'):
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
            memcache[self.key_format(k)] = int(v)
        
        if param == 'data':
            return memcache
        elif param == 'groups':
            return {'meminfo': {'name': 'meminfo', 'parents': ['root']}}
            
        mets = dict()
        for i in memcache.keys():
            mets[self.key_format(i)] = {'name': i,
                              'unit': 'kB',
                              'parents': ['meminfo']}
        
        return mets


    def get_data(self):
        return MemInfo.meminfo()

if __name__ == "__main__":
    c = MemInfo()
    c.run()






