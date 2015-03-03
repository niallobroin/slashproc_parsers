#!/usr/bin/env python

import re
import os
import glob
from itertools import chain
from collections import defaultdict
from sp_parser.basic_sp_parser import BasicSPParser


class Kernel(BasicSPParser):

    KERNEL = "/proc/sys/kernel"

    @staticmethod
    def get_vars():
        pass

    @staticmethod
    def get_groups():
        pass

    @staticmethod
    def get_data():
        """Parse /proc/sys/kernel directory and its subdirs.

        Each non-directory file name is treated as variable name. Accordingly,
        file's content is treated as variable value. All groups in result
        dictionary preserve parent-child relations.

        Returns:
            tree (dict): nested dictionaries with system variables
        """

        tree = dict()
        common = os.path.split(Kernel.KERNEL)[0] + '/'

        for thedir, subdirs, files in os.walk(Kernel.KERNEL):
            relative_to_root = thedir.replace(common, '')
            parts = relative_to_root.split('/')

            d = tree

            # index nested dictionaries
            for key in parts[:-1]:
                d = d[key]

            deepest_dir = parts[-1]

            # deepest dictionary level is index by deepest directory name
            d[deepest_dir] = dict()

            for entry in files:
                with open(os.path.join(thedir, entry)) as f:
                    d[deepest_dir][entry] = f.read().replace('\n', '')

        return tree


if __name__ == "__main__":
    k = Kernel()
    k.get_data()