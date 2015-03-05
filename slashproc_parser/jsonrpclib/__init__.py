from slashproc_parser.jsonrpclib.config import Config
config = Config.instance()
from slashproc_parser.jsonrpclib.history import History
history = History.instance()
from slashproc_parser.jsonrpclib.jsonrpc import Server, MultiCall, Fault
from slashproc_parser.jsonrpclib.jsonrpc import ProtocolError, loads, dumps
