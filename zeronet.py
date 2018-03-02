#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		config                      Get or set config values
		wrapperkey                  Return wrapper key of a site or find a site by wrapper key

		Use 'help <command>' or 'help <command> <subcommand>' for more info
	"""

	def action(self, *args, **kwargs):
		if len(args) == 0:
			if len(kwargs) == 0:
				raise Callable.Redirect("help")
			elif len(kwargs) == 1 and "help" in kwargs:
				raise Callable.SubCommand("help")
			else:
				sys.stderr.write("Why are you passing named arguments to this command? Try 'help' instead.\n")
		else:
			raise Callable.SubCommand

	def actionConfig(self, *args, **kwargs):
		"""
			Get or set config values

			Subcommands:
			config list                 Print list of all saved values as newline-separated values
			config set                  Set config value
			config get                  Get config value
			config remove               Remove config value
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

	def actionConfigGet(self, name):
		"""
			Get config value

			Usage:
			config get <name>           Print config variable <name>. <name> can be dot-separated.
		"""

		print config.get(name)

	def actionConfigRemove(self, name):
		"""
			Remove config variable

			Usage:
			config remove <name>        Remove config variable <name>. All the following 'config get' will be rejected.
			                            <name> can be dot-separated.
		"""

		config.remove(name)


	def actionWrapperkey(self, search, reverse=False):
		"""
			Return wrapper key of a site or find a site by wrapper key

			Usage:
			wrapperkey <address>        Print wrapper key of a site by address
			wrapperkey <key> --reverse  Print site address by wrapper key
		"""

		try:
			if reverse == False:
				print Site.get_wrapperkey(config["data_directory"], search)
			else:
				print Site.find_by_wrapperkey(config["data_directory"], search)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])

ZeroNet(argv)