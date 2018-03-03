#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.addresses as Addresses
from zeronet_lib.zerowebsocket import ZeroWebSocket

class ZeroHello(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		site                        Edit or get some info about site

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

	def actionSite(self, *args, **kwargs):
		"""
			Edit or get some info about site

			Subcommands:
			site pause                  Pause site
			site resume                 Resume site
		"""

		raise Callable.SubCommand

	def actionSitePause(self, address):
		"""
			Pause site

			Usage:
			site pause <address>        Stop seeding <address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				ws.send("sitePause", address=address)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionSiteResume(self, address):
		"""
			Resume site

			Usage:
			site resume <address>       Resume seeding <address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				ws.send("siteResume", address=address)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])
	def getAddress(self):
		return config.get("homepage", Addresses.ZeroHello)

	def connect(self, site):
		wrapper_key = Site.getWrapperkey(self.getDataDirectory(), site)

		address = config.get("server.address", "127.0.0.1")
		port = config.get("server.port", "43110")
		secure = config.get("server.secure", False)

		return ZeroWebSocket(wrapper_key, "%s:%s" % (address, port), secure)

try:
	sys.exit(ZeroHello(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)