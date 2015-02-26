#!/usr/bin/env python
"""
/proc/thedir
"""

from sp_parser.basic_sp_parser import BasicSPParser


class TheParser(BasicSPParser):

    THEDIR = "/proc/thedir"

    def __init__(self):
        super(TheParser, self).__init__(self)

    @staticmethod
    def get_groups():
        """
        REMOVE THIS DOCSTRING AND CREATE ONE APPROPIATE TO THE PARSER

        Ensure first group is the parser name and its parent is ['root']
        Ensure group labels are unique
            if there are multiple then subscript with number etc...
        Ensure each group has a parent, and parents is a list

        :rtype: dict
        """
        groups = {
            'theparser': {'label': "Formatted Long Parser Label",
                          'desc': "Description of the parser",
                          'parents': ['root']},

            'group1': {'label': 'The first group',
                       'parents': ['theparser']},

            'group2': {'label': 'The second group',
                       'parents': ['group1'],
                       'desc': "Desc recommended but not necessary"}
             }

        return groups

    @staticmethod
    def get_vars():
        """
        REMOVE THIS DOCSTRING AND CREATE ONE APPROPIATE TO THE PARSER

        Ensure var labels are all lower case, contain underscores (not dash)
            and the following chars are not permitted "()[]/\ "
        Ensure every var has a unit where appropriate

        :rtype: dict
        """
        vars = {
            'var1': {'label': 'The first Variable'},

            'var2': {'label': 'The Second Variable',
                     'unit': 'kB', 
                     'desc': 'Description recommended but not necessary'}
            }
        return vars

    @staticmethod
    def get_data():
        """
        REMOVE THIS DOCSTRING AND CREATE ONE APPROPIATE TO THE PARSER

        Ensure first group is the parser name
        Ensure return adheres to the groups structure
        Ensure all groups are present in the groups dict
        Ensure all vars adhere to the var format
        Ensure all vars are present in the vars dict
        Ensure every value is a string

        :rtype: dict
        """
        data = {'theparser': {
                                'group1': {
                                            'group2': {'var1': 'val1',
                                                       'var2': 'val2'},
                                            }
                         }
                     }

        return data



if __name__ == "__main__":
    c = TheParser()
    c.test_parse()
