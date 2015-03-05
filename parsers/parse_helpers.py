import os


def traverse_directory(path, verbose=False):
    """Helper for /proc/sys parsers.

    Walks over specified directory and collects it's files contents
    into tree-like structure.
    """

    tree = dict()
    parents = dict()
    thevars = set()
    common = os.path.split(path)[0] + '/'

    for thedir, subdirs, files in os.walk(path):
        relative_to_root = thedir.replace(common, '')
        parts = relative_to_root.split('/')

        d = tree

        # index nested dictionaries
        for key in parts[:-1]:
            d = d[key]

        deepest_dir = parts[-1]

        for subdir in subdirs:
            _, child = os.path.split(subdir)
            parents[child] = deepest_dir

        # deepest dictionary level is indexed by deepest directory name
        d[deepest_dir] = dict()

        for entry in files:
            thevars.add(entry)
            parents[entry] = deepest_dir
            varpath = os.path.join(thedir, entry)
            try:
                with open(varpath) as f:
                    d[deepest_dir][entry] = f.read().replace('\n', '')
            except IOError:
                if verbose:
                    print 'Permission denied: ' + varpath

    return tree, parents, thevars