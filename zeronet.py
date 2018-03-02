#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv
from lib.config import config

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                    Print this help
		config                  Get or set config values

		Use 'help <command>' or 'help <command> <subcommand>' for more info
	"""

	def actionHelp(self, cmd="", *sub):
		if cmd == "help":
			self.actionHelp("", *sub)
		else:
			super(ZeroNet, self).actionHelp(cmd, *sub)

	def actionConfig(self, prefix=None):
		"""
			Print list of all saved values as newline-separated values

			Usage:
			config                  Print all values
			config <prefix>         Print all values beginning with <prefix>
		"""

		print "\n".join(filter(lambda name: name.startswith(prefix), config.list()))

ZeroNet(argv[0] if argv != [] else "help", argv[1:])