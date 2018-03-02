#!/usr/bin/env python

import sys
from lib.args import argv

class ZeroNet(object):
	def __init__(self, cmd, args):
		try:
			handler = getattr(self, "action" + cmd[0].upper() + cmd[1:])
		except AttributeError:
			all_commands = [name[6].lower() + name[7:] for name in dir(self) if name.startswith("action")]
			sys.stderr.write("Unknown command %s. Allowed commands are: %s\n" % (cmd, ", ".join(all_commands)))
			return

		handler()

	def actionHelp(self):
		print "Commands:"
		print "help            Print this help"

ZeroNet(argv[0] if argv != [] else "help", argv[1:])