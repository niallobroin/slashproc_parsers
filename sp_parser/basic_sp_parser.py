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
        return repr(self.value)



class BasicSPParser(object):
    """
    Base class for any sp_parser
    """

    def __init__(self, *args, **kwargs):
        super(BasicSPParser, self).__init__()

    @staticmethod
    def get_groups():
        """
        This method must be overridden by the colector class
        """
        raise NotImplementedError("Method get_groups not defined")

    @staticmethod
    def get_vars():
        """
        This method must be overridden by the colector class
        """
        raise NotImplementedError("Method get_vars not defined")

    @staticmethod
    def get_data():
        """
        This method must be overridden by the colector class
        """
        raise NotImplementedError("Method get_data not defined")

    def cl(self):
        """
        Gets the class of the lowest class, ie the class instantiated
        """
        return self.__class__.__name__.lower()

    def get_class(self):
        """
        Gets the class of the lowest class, ie the class instantiated
        """
        return self.cl()

    def validate_groups(self, debug=False):
        """
        This method may be called by other classes to ensure the test_parser
        is returning correctly formatted results. 

        Ensure group names are unique
            if there are multiple then subscript with number etc...
        Ensure var names are all lower case, contain underscores (not dash)
            and the following chars are not permitted "()[]/\ "
        Ensure each group has a parent, and parents must be list
        Ensure at least one group has parent 'root'

        Example {'group1': {'name': 'The first group', parents: ['root']},
                 'group2': {'name': 'The second group', parents: ['group1'],
                            'desc':'Desc recommended but not necessary'}
                 }
        :param debug: Debug flag to print debug output
        :rtype bool:
        """
        errors = list()
        debug_msg = ["Validating Groups"]

        groups = self.get_groups()
        if not isinstance(groups, dict):
            return False

        parents = list()
        for g in groups:
            if g != self.key_format(g):
                errors.append("Group '%s' not formatted correctly" % g)
            
            if not isinstance(groups[g], dict):
                return False

            if 'name' not in groups[g]:
                errors.append("Error 'name' not defined for group '%s'" % g)
        
            if 'desc' not in groups[g]:
                debug_msg.append("'desc' not defined for group '%s'" % g)

            if 'parents' not in groups[g]:
                errors.append("Error 'parents' not defined for group '%s'" % g)

            #parents must be list
            if not isinstance(groups[g]['parents'], list):
                errors.append("Error 'parents' must be a list for group '%s'" % g)

            #Flatten parents
            parents.extend(groups[g]['parents'])

        #Ensure at least one, group has parent root
        if 'root' not in parents:
            errors.append("Error One and only one, group must have a parent 'root'")
        parents.remove('root')

        #Except for root, every parents must be in groups
        #TODO should include group of parent in error message
        for i in parents:
            if i not in groups:
                errors.append("Error parent '%s' not in groups" % i)

        if debug:
            for i in debug_msg:
                print i
            for i in errors:
                print i

        return False if errors else True
    

    def validate_vars(self, debug=False):
        """
        This method may be called by other classes to ensure the test_parser
        is returning correctly formatted results. 

        Ensure var names are all lower case, contain underscores (not dash)
            and the following chars are not permitted "()[]/\ "
        Ensure every var has a unit

        Example: {'var1': {'name': 'The first Variable', 'unit': ''},
                  'var2': {'name': 'The Second Variable', 'unit': 'kB', 
                            'desc': 'Description recommended but not necessary'}
                  }
        :param debug: Debug flag to print debug output
        :rtype bool:
        """
        errors = list()
        debug_msg = ["Validating Vars"]

        thevars = self.get_vars()
        if not isinstance(thevars, dict):
            return False
        for v in thevars:
            if v != self.key_format(v):
                errors.append("Var '%s' not formatted correctly" % v)

            if not isinstance(thevars[v], dict):
                return False

            if 'name' not in thevars[v]:
                errors.append("Error 'name' not defined for var '%s'" % v)
        
            if 'unit' not in thevars[v]:
                errors.append("Error 'unit' not defined for var '%s'" % v)
        
            if 'desc' not in thevars[v]:
                debug_msg.append("'desc' not defined for var '%s'" % v)

        if debug:
            for i in debug_msg:
                print i
            for i in errors:
                print i

        return False if errors else True

    def validate_data(self, debug=False):
        """
        This method may be called by other classes to ensure the test_parser
        is returning correctly formatted results.

        Ensure return_dict adheres to the groups structure
        Ensure all groups are present in the groups dict
        Ensure all vars adhere to the var format
        Ensure all vars are present in the vars dict
        Ensure every value is a string

        Example: {'group1': {
                            'group2': {'var1': 'val1',
                                       'var2': 'val2'},
                            }
                 }
        :param debug: Debug flag to print debug output
        :rtype bool:
        """

        errors = list()
        debug_msg = ["Validating parser %s" % self.cl()]

        groups = self.get_groups().keys()
        thevars = self.get_vars().keys()
        data = self.get_data()

        #Recursion function to validate and help debug the parser
        def validate_sub(subdata):

            for k in subdata.keys():

                if k != self.key_format(k):
                    errors.append("Error key format does not confirm")

                if isinstance(subdata[k], dict) and k not in groups:
                    errors.append("Error group '%s' not found" % k)

                elif isinstance(subdata[k], dict) and k in groups:

                    debug_msg.append("Found group '%s'" % k)
                    groups.remove(k)

                    debug_msg.append("Calling Recursive again")
                    validate_sub(subdata[k])
            
                elif isinstance(k, str) and k not in thevars:
                    errors.append("Variable '%s' not found" % k)

                elif isinstance(k, str) and k in thevars:
                    debug_msg.append("Found Variable %s" % k)
                else:
                    raise Exception

        #Call the rucursion function above
        debug_msg.append("Starting Recursion")
        validate_sub(data)

        if debug:
            for i in debug_msg:
                print i
            for i in errors:
                print i

        return False if errors else True

    def validate_parser(self, debug=False):
        g = self.validate_groups(debug=debug)
        v = self.validate_vars(debug=debug)
        d = self.validate_data(debug=debug)
        if not g or not v or not d:
            return False
        return True

    def pp_groups(self):
        """
        Pretty prints the data
        """
        pp = pprint.PrettyPrinter(indent=2, depth=10)
        pp.pprint(self.get_groups())

    def pp_vars(self):
        """
        Pretty prints the data
        """
        pp = pprint.PrettyPrinter(indent=2, depth=10)
        pp.pprint(self.get_vars())

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
        return txt.strip('()[]').replace(' ', '_').replace('-', '_').replace('/', '_').lower()

    def test_parse(self):
        """
        Prints out some data to test if the sp_parser is running
        """

        print "\n\n Groups"
        self.pp_groups()

        print "\n\n Vars"
        self.pp_vars()

        print "\n\n Data"
        self.pp_data()

        print "\n\n"
        self.validate_parser()


def main():
    """
    Main
    """
    exit("Run the parser module not this base class")


if __name__ == "__main__":
    main()
