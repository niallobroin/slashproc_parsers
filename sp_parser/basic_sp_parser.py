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

class MSG(object):
    debug1 = "Validating parser %s"
    debug2 = "Found group '%s'"
    debug3 = "Calling Recursive again"
    debug4 = "Found Variable %s"
    debug5 = "Starting Recursion"
    debug6 = "Validating Groups"
    debug7 = "'desc' not defined for group '%s'"
    debug8 = "'desc' not defined for var '%s'"
    debug9 = "Recommend 'label' be defined for var '%s'"
    debug10 = "Recommend 'unit' be defined for var '%s'"
    debug11 = "Recommend 'label' be defined for group '%s'"

    err1 = "Error key format does not conform"
    err2 = "Error group '%s' not found"
    err3 = "Variable '%s' not found"
    err4 = "Group '%s' not formatted correctly"

    err6 = "Error 'parents' not defined for group '%s'"
    err7 = "Error 'parents' must be a list for group '%s'"
    err8 = "Error One and only one, group must have a parent 'root'"
    err9 = "Error parent '%s' not in groups"
    err10 = "Var '%s' not formatted correctly"


    err13 = "Group '%s' must be dict"
    err14 = "get_var must return a dict"
    err15 = "First Level in data should be the class name"
    err16 = ("One group should be called after the parser"
                            "name and it must have parent 'root'")

    @classmethod
    def debug(cls, num, param=''):
        msg = getattr(cls, 'debug%s' % num)
        return msg % param if '%s' in msg else msg

    @classmethod
    def err(cls, num, param=''):
        msg = getattr(cls, 'err%s' % num)
        return msg % param if '%s' in msg else msg


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
        Recommend every group has a label
        Recommend every group has a description

        Example:
            'theparser': {'label': "Formatted Long Parser Label",
                          'desc': "Description of the parser",
                          'parents': ['root']},

            'group1': {'label': 'The first group',
                       'parents': ['theparser']},

            'group2': {'label': 'The second group',
                       'parents': ['group1'],
                       'desc': "Desc recommended but not necessary"}
             }

        :param debug: Debug flag to print debug output
        :rtype bool:
        """
        errors = list()
        debug_msg = [MSG.debug(6)]
        groups = self.get_groups()
        if not isinstance(groups, dict):
            return False

        parents = list()
        for g in groups:
            if g != self.key_format(g):
                errors.append(MSG.err(4, g))

            if not isinstance(groups[g], dict):
                errors.append(MSG.err(13, g))

            if 'label' not in groups[g]:
                debug_msg.append(MSG.debug(11, g))

            if 'desc' not in groups[g]:
                debug_msg.append(MSG.debug(7, g))

            if 'parents' not in groups[g]:
                errors.append(MSG.err(6, g))

            #parents must be list
            if not isinstance(groups[g]['parents'], list):
                errors.append(MSG.err(7, g))

            #Gather parents
            parents.extend(groups[g]['parents'])

         #Ensure one and only one group has parent root
        if parents.count('root') != 1:
            errors.append(MSG.err(8))

        #Except for root, every parents must be in groups
        #TODO should include group of parent in error message
        parents.remove('root')
        for i in parents:
            if i not in groups:
                errors.append(MSG.err(9, i))

        #Ensure theres a group called 'theparser' and it has parent 'root'
        if (self.cl() not in groups or
            groups[self.cl()]['parents'] != ['root']):
            errors.append(MSG.err(16))


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
        Recommend every var has a label
        Recommend every var has a unit
        Recommend every var has a description

        Example:
            'var1': {'label': 'The first Variable'},

            'var2': {'label': 'The Second Variable',
                     'unit': 'kB',
                     'desc': 'Description recommended but not necessary'}
            }
        :param debug: Debug flag to print debug output
        :rtype bool:
        """
        errors = list()
        debug_msg = ["Validating Vars"]
        thevars = self.get_vars()

        if not isinstance(thevars, dict):
            errors.append(MSG.err(14))

        for v in thevars:
            if v != self.key_format(v):
                errors.append(MSG.err(10, v))

            if not isinstance(thevars[v], dict):
                errors.append(MSG.err(15, g))

            if 'label' not in thevars[v]:
                debug_msg.append(MSG.debug(9, v))

            if 'unit' not in thevars[v]:
                debug_msg.append(MSG.debug(10, v))

            if 'desc' not in thevars[v]:
                debug_msg.append(MSG.debug(8, v))

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

        Example:
            'theparser': {'label': "Formatted Long Parser Label",
                          'desc': "Description of the parser",
                          'parents': ['root']},

            'group1': {'label': 'The first group',
                       'parents': ['theparser']},

            'group2': {'label': 'The second group',
                       'parents': ['group1'],
                       'desc': "Desc recommended but not necessary"}
             }
        :param debug: Debug flag to print debug output
        :rtype bool:
        """

        errors = list()
        debug_msg = [MSG.debug(1, self.cl())]

        groups = self.get_groups().keys()
        thevars = self.get_vars().keys()
        data = self.get_data()

        if len(data.keys()) > 1 or data.get(self.cl(), False):
            errors.append(MSG.err(16))

        #Recursion function to validate and help debug the parser
        def validate_sub(subdata):

            for k in subdata.keys():
                if k != self.key_format(k):
                    errors.append(MSG.err(1))

                if isinstance(subdata[k], dict) and k not in groups:
                    errors.append(MSG.err(2, k))

                elif isinstance(subdata[k], dict) and k in groups:
                    debug_msg.append(MSG.debug(2, k))
                    groups.remove(k)

                    debug_msg.append(MSG.debug(3))
                    validate_sub(subdata[k])

                elif isinstance(k, str) and k not in thevars:
                    errors.append(MSG.err(3, k))

                elif isinstance(k, str) and k in thevars:
                    debug_msg.append(MSG.debug(4, k))
                else:
                    raise Exception

        #Call the rucursion function above
        debug_msg.append(MSG.debug(5))
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

    @staticmethod
    def label_format(name):
        """
        Helper for the sub classes
        """
        return name.replace('_', ' ').title()

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
