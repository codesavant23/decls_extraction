"""
Python autonomous component which gives the ability to extract:
- Functions
- Methods
- Classes

View the enumerator `ECodeParserTool` for the currently implemented, and available, parsers.
"""

from . import classdecls_extractor
from . import moddecls_extractor

from ._private.e_parser_tool import ECodeParserTool
