#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv

class ZeroNet(Callable):
	def actionHelp(self, cmd="help"):
		if cmd == "help":
			print "Commands:"
			print "help            Print this help"
		else:
			print "Unknown topic '%s'" % cmd

ZeroNet(argv[0] if argv != [] else "help", argv[1:])