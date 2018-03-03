#!/usr/bin/env python

import sys, os, signal as os_signal
import sqlite3, json
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
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

	def actionResolve(self, domain):
		"""
			Get address of a site by its domain

			Usage:
			resolve <domain>            Print address of the site
		"""

		try:
			print Site.findByDomain("%s/%s/data/names.json" % (self.getDataDirectory(), config.get("zeroname.registry", Addresses.ZeroName)), domain)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])

try:
	sys.exit(ZeroName(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)