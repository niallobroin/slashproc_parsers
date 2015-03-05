"""
Multithreaded JSONRPCServer example

addr = "localhost:8848"
requests.post(addr, data='{"method": "get_data", "params":{"parser": "cpuinfo", "get": "model_name"}, "id":456}').json()

curl -X POST http://localhost:8848 -d '{"method": "get_data", "id":"2", "params":{"dir":"/proc/uptime"}}'

reply
{"jsonrpc": "2.0", "result": {"uptime": {"found": {"uptime": 55}}}, "id": "2"}
"""

import sys
import parsers

from SocketServer import ThreadingMixIn
from slashproc_parser.jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_PORT = 8848

#do debug mode and
#prevent returning errors through to the json parser
DEBUG = True


class SimpleThreadedJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
    pass


class ERR():
    err1 = "Parser not Found"
    err2 = "get param '%s' not found in groups or vars"

    @classmethod
    def msg(cls, num, param=''):
        msg = getattr(cls, 'err%s' % num)
        msg % param if '%s' in msg else msg
        return {'err': num, 'msg':msg}


def import_parsers():
    """
    Imports the parsers
    """
    parsers_name = list()
    parsers_cls = dict()


    for modpy in parsers.__all__:
        mod = __import__('parsers.' + modpy, fromlist=[modpy])
        classes = [getattr(mod, modpy) for modpy in dir(mod)
            if isinstance(getattr(mod, modpy), type) and modpy != 'sp_parser_template.py']

        for cls in classes:
            parsers_name.append(cls.__name__.lower())
            parsers_cls[cls.__name__.lower()] = cls

    return (parsers_name, parsers_cls)


def input_validation(path, parser, get):

    SEPARATORS = "., |"

    # Will not fail on dot locations
    def make_list(txt):
        if not txt:
            return list()
        if isinstance(txt, list):
            txt = '/'.join(txt) 
        for i in SEPARATORS:
            txt = txt.replace(i, '/')
        txt = [i for i in txt.split('/') if i != '']
        return txt

    # if path, ignore the rest
    path = make_list(path)
    if path:
        if path[0] == 'proc':
            path.pop(0)
        return path[0], path[1:]

    parser = make_list(parser)
    if not parser:
        return  None, None
    else:
        if parser[0] == 'proc':
            parser.pop(0)

    get = make_list(get)
    get.extend(parser[1:])

    return parser[0], get

def get_groups(path=None, parser=None, get=None):
    """
    Method to return one or more group descriptors

    {"method": "get_groups",
     "params": {
        "path": "/core1",
        #or
        "parser": "/proc/cpuinfo|cpuinfo",
        "get": "core1"
    }}

    Usage:
    path: location to single var or group
    or
    parser: the parser
    get: a csv string or list of groups

    """
    names, classes = import_parsers()

    parser, get = input_validation(path, parser, get)

    if not parser or parser not in names:
        return ERR.msg(1)
    groups = classes[parser].get_groups()

    if not get or 'all' in get or 'star' in get:
        return {'found': groups}

    #TODO if desc just return desc
    ret = dict()
    for g in get:
        if g in groups:
            if 'found' in ret:
                ret['found'][g] = groups[g]
            else:
                ret['found'] = {g: groups[g]}
        else:
            if 'notfound' in ret:
                notfound.append(g)
            else:
                ret['notfound'] = [g]
    return ret

def get_vars(path=None, parser=None, get=None):
    """
    Method to return the var descriptors

    {"method": "get_vars",
     "params": {
        "path": "cpuinfo/v1",
        #or
        "parser": "cpuinfo",
        "get": "v1 v2"
    }}

    Usage:
    path: location to single var

    parser: the parser
    get: a csv string or list of vars
    """

    names, classes = import_parsers()

    parser, get = input_validation(path, parser, get)

    if not parser or parser not in names:
        return ERR.msg(1)
    thevars = classes[parser].get_vars()

    if not get or 'all' in get or 'star' in get:
        return {'found': thevars}

    ret = dict()
    for g in get:
        if g in thevars:
            if 'found' in ret:
                ret['found'][g] = thevars[g]
            else:
                ret['found'] = {g: thevars[g]}
        else:
            if 'notfound' in ret:
                notfound.append(g)
            else:
                ret['notfound'] = [g]
    
    return ret

def get_data(path=None, parser=None, get=None):
    """
    Method to return the data

    {"method": "get_data",
     "params": {
        "path": "/core1",
        #or
        "parser": "cpuinfo",
        "get": "g1, g2, var1, var2"
    }}

    Usage:
    path: location to single var or group

    parser: the parser
    get: a csv string or list of groups and vars

    """
    names, classes = import_parsers()

    parser, get = input_validation(path, parser, get)

    if not parser or parser not in names:
        return ERR.msg(1)
    groups = classes[parser].get_groups()
    vars = classes[parser].get_vars()


    data = classes[parser].get_data()

    if not get:
        return {'found': data}


    ret = dict()
    found = list()
    def recurse_dict(dct, pth, get):
        for k in dct.keys():
            if k in get:
                if k not in found:
                    found.append(k)
                ret[pth+'/'+k] = dct[k]
            elif isinstance(dct[k], dict):
                recurse_dict(dct[k], pth+'/'+k, get)

    recurse_dict(data, '', get)

    for i in found:
        get.remove(i)
   
    retdict = dict()
    if ret:
        retdict['found'] = ret
    if get:
        retdict['notfound'] = get

    return retdict

def main():
    a, b = import_parsers()
    server = SimpleThreadedJSONRPCServer(('localhost', SERVER_PORT))
    server.register_function(get_data)
    server.register_function(get_groups)
    server.register_function(get_vars)
    server.serve_forever()

if __name__ == '__main__':
    main()
