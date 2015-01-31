#!/usr/bin/env python
"""

/proc/thedir


"""

from basic_sp_parser import BasicSPParser


class TheDir(BasicSPParser):

    THEDIR = "/proc/thedir"

    def __init__(self):
        super(TheDir, self).__init__(self)

    @staticmethod
    def get_groups():
        """
        
            paste rules here

        """

        return groups_dict

    @staticmethod
    def get_vars():
        """

        PAste the rules here

        """
        
        return vars_dict

    @staticmethod
    def get_data():
        """
        """

        return data_dict



if __name__ == "__main__":
    c = TheDir()
    c.run()




