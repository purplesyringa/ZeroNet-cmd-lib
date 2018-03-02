#!/usr/bin/env python

import sys, inspect
from lib.callable import Callable
from lib.args import argv

class ZeroNet(Callable):
	"""
		Commands:
		help            Print this help
	"""

	def actionHelp(self, cmd="help"):
		if cmd == "help":
			print inspect.cleandoc(ZeroNet.__doc__)
		else:
			print "Unknown topic '%s'" % cmd

ZeroNet(argv[0] if argv != [] else "help", argv[1:])