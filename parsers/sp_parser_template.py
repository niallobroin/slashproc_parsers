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

    Ensure group names are unique
        if there are multiple then subscript with number etc...
    Ensure each group has a parent, and parents must be list
    Ensure at least one group has parent 'root'

    Example {'group1': {'name': 'The first group', parents: ['root']},
         'group2': {'name': 'The second group', parents: ['group1'],
                    'desc':'Desc recommended but not necessary'}
         }

    :rtype: dict
    """

    return groups_dict

@staticmethod
def get_vars():
    """
    REMOVE THIS DOCSTRING AND CREATE ONE APPROPIATE TO THE PARSER

    Ensure var names are all lower case, contain underscores (not dash)
        and the following chars are not permitted "()[]/\ "
    Ensure every var has a unit

    Example: {'var1': {'name': 'The first Variable', 'unit': ''},
              'var2': {'name': 'The Second Variable', 'unit': 'kB', 
                        'desc': 'Description recommended but not necessary'}
              }

    :rtype: dict
    """
    return vars_dict

@staticmethod
def get_data():
    """
    REMOVE THIS DOCSTRING AND CREATE ONE APPROPIATE TO THE PARSER

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

    :rtype: dict
    """
    return data_dict



if __name__ == "__main__":
    c = TheParser()
    c.test_parse()