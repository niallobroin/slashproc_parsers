#!/usr/bin/env python
"""
The Base class for every sp_parser

This is primarily to help Developers write and test 
individual sp_parsers.

"""
import pprint




class SPParserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return rept(self.value)



class BasicSPParser(object):
    """
    Base class for any sp_parser
    """

    def __init__(self, *args, **kwargs):
        super(BasicSPParser, self).__init__()

        self.vars = dict()
        self.groups = dict()


    @staticmethod
    def get_vars():
        """
        This method must be overridden by the colector class
        """
        raise SPParserError("Method get_vars not defined")

    @staticmethod
    def get_groups():
        """
        This method must be overridden by the colector class
        """
        raise SPParserError("Method get_groups not defined")


    def _validate_subclass(self):
        """
        Validates the functions and formats of results are OK
        """
        return True

    def cl(self):
        """
        Gets the class of the lowest class, ie the class instantiated
        """
        return self.__class__.__name__.lower()

    def get_class(self):
        """
        Gets the class of the lowest class, ie the class instantiated
        """
        return self.__class__.__name__.lower()


    def test_groups(self):
        """
        Ensure group names are unique
            if there are multiple then subscript with number etc...

        Ensure each group has a parent, and parents must be list

        Ensure at least one group has parent 'root'
        """

        groups = self.get_groups()
        
        if not isinstance(groups, dict):
            return False

        #Ensure every group has name, and its a string
        names = [groups[i].get('name', 'ERRORERROR') for i in groups]
        if 'ERRORERROR' in names:
            return False

        #Ensure every group has parents
        parents = [groups[i].get('parents', 'ERRORERROR') for i in groups]
        if 'ERRORERROR' in parents:
            return False
        
        #parents must be list
        if False in [isinstance(i, list) for i in parents]:
            return False

        #Flatten parents
        flat_parents = set([j for i in parents for j in i])

        #Ensure at least one, group has parent root
        if 'root' not in flat_parents:
            return False
        flat_parents.remove('root')

        #Except for root, every parents must be in groups
        for i in parents:
            if i not in groups:
                return False

        return True



    def test_vars(self):
        """
        Vars name must be unique
        Ensure 'unit' on each var
        """

        thevars = self.get_groups()
        
        if not isinstance(thevars, dict):
            return False

        #Ensure every var  has name, and its a string
        names = [thevars[i].get('name', 'ERRORERROR') for i in thevars]
        if 'ERRORERROR' in names:
            return False


            return True

    def test_sp_parser(self):
        """
        This method may be called by other classes to ensure the test_parser
        is returning correctly formatted results. 
        """

        print "Testing SPParser %s" % self.cl()

        groups = self.get_groups()
        thevars = self.get_vars()
        data = self.get_data()

        #Recursion function to clean the testcache
        def test_clean_testcache(selfcache, grp):
            """
            Empties the self.cache
            """
            print "Testing items %s" % grp.keys()
            

            for k in grp.keys():

                if isinstance(grp[k], dict) and k not in groups:
                    #its NOT a monitored group
                    #del grp[k]
                    print "Group not found %s" % k

                elif isinstance(grp[k], dict) and k in groups:
                    #its a wanted group

                    if k not in selfcache:
                        data[k] = dict()

                    print "Calling Recursive again"
                    test_clean_testcache(selfcache[k], grp[k])
            

                elif not isinstance(grp[k], dict) and k not in thevars:
                    print "Group not found %s" % k
                else:
                    if k not in selfcache:
                        selfcache[k] = list()
                    
                    #print "Appending %s" % grp[k]
                    selfcache[k].append(grp[k])
            

        #Call the rucursion function above
        print "Starting Recursion"
        test_clean_testcache(data[self.cl()], testcache)

    def pp_data(self):
        """
        Pretty prints the data
        """
        pp = pprint.PrettyPrinter(indent=2, depth=10)
        pp.pprint(self.get_data())



    @staticmethod
    def key_format(txt):
        """
        Helper for the sub classes
        """
        t = txt.replace(' ', '-').replace('_', '-').replace('/', '-').lower()
        return t.replace(')', '').replace('(', '').replace('[', '').replace(']', '')



    def run(self):
        """
        Prints out some data to test if the sp_parser is running
        """

        print 'groups', self.get_groups()

        print '\n'
        print 'vars', self.get_vars()

        print '\n\n'
        print 'data', self.get_data()


        print '\n\n'
        print self.pp_data()


        print '\n\n'
        print "Test SPParser", self.test_sp_parser()


def main():
    """
    Main
    """
    exit("Run the sp_parser module not this base class")


if __name__ == "__main__":
    main()
