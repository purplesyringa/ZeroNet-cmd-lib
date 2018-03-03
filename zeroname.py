#!/usr/bin/env python

import sys, os, signal as os_signal
import sqlite3, json
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.addresses as Addresses

class ZeroName(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		resolve                     Get address of a site by its domain

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
				return 2
		else:
			raise Callable.SubCommand

	def actionResolve(self, address):
		"""
			Get address of a site by its domain

			Usage:
			resolve <address>           Print address of the site
		"""

		raise NotImplementedError

try:
	sys.exit(ZeroName(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)