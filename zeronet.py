#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv

class ZeroNet(Callable):
	def actionHelp(self):
		print "Commands:"
		print "help            Print this help"

ZeroNet(argv[0] if argv != [] else "help", argv[1:])