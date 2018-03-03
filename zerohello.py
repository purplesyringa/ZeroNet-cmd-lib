#!/usr/bin/env python

import sys, os, signal as os_signal
import sqlite3, json
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.addresses as Addresses

class ZeroHello(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help

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

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])
	def getAddress(self):
		return config.get("homepage", Addresses.ZeroHello)

try:
	sys.exit(ZeroHello(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)