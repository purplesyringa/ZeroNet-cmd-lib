#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv
from lib.config import config

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		config                      Get or set config values

		Use 'help <command>' or 'help <command> <subcommand>' for more info
	"""

	def actionConfig(self, *args):
		"""
			Get or set config values

			Subcommands:
			config list                 Print list of all saved values as newline-separated values
			config set                  Set config value
		"""

		raise Callable.SubCommand

	def actionConfigList(self, prefix=""):
		"""
			Print list of all saved values as newline-separated values

			Usage:
			config list                 Print all values
			config list <prefix>        Print all values beginning with <prefix>
		"""

		print "\n".join(filter(lambda name: name.startswith(prefix), config.list()))

	def actionConfigSet(self, name, value):
		"""
			Set config value

			Usage:
			config set <name> <value>   Set config variable <name> to <value>. <name> can be dot-separated.
		"""

		config.set(name, value)

ZeroNet(argv[0] if argv != [] else "help", argv[1:])