#!/usr/bin/env python
#!/usr/bin/env python


from basic_sp_parser import BasicSPParser


class Load(BasicSPParser):
    """
    Very basic parser built for Gallelio
    """

    def __init__(self):
        super(Load, self).__init__(self)


        self.re_cpu = re.compile('(.*?) ')





    @staticmethod
    def get_groups():
        """
        Static method to define vars that that parser can parse
        #Will probably be a class later.
        """
        GROUPS = {
            'cpu': {'name': 'CPU', 'parents': ['root']}, 
                }#end of group
        
    @staticmethod
    def get_vars():
        """
        Static method to define vars that that parser can parse
        #Will probably be a class later.
        """
        METRICS = dict()

        parents = ['root']
        METRICS['load-avg'] = {'name': 'cpu load average',
                                   'parents': parents,
                                   'unit': '%'}

        grps = Performance.get_groups()
        net = [i for i in grps if 'net' in grps[i]['parents'] ] 



        return METRICS

    def read_proc(self, filename, regex, n):
        with open(filename, 'r') as f:
            for line in f:
                found = re.search(regex, line)
                if found:
                    return found.groups()[n]




    def get_data(self):
        """

        """



        return {'load-avg': self.read_proc("/proc/loadavg", self.re_cpu, 0)}





if __name__ == "__main__":
    c = Load()
    c.run()
