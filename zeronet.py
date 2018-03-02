#!/usr/bin/env python

import sys, inspect
from lib.callable import Callable
from lib.args import argv

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help            Print this help
	"""

ZeroNet(argv[0] if argv != [] else "help", argv[1:])