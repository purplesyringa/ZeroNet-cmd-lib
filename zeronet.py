#!/usr/bin/env python

import sys
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.user as User
from zeronet_lib.zerowebsocket import ZeroWebSocket

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		config                      Get or set config values
		wrapperkey                  Return wrapper key of a site or find a site by wrapper key
		socket                      Send request to ZeroWebSocket
		user                        Configure users

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
			return 1

	def actionSocket(self, site, cmd, *args, **kwargs):
		"""
			Send request to ZeroWebSocket

			Usage:
			socket <site> <cmd>         Send command without arguments to site <site>
			socket <site> <cmd> 1 2 3   Send command <cmd> with arguments 1, 2 and 3
			socket <site> <cmd> --1 2   Send command <cmd> with arguments 1=2 and 3=True
			                    --3
		"""

		if len(args) > 0 and len(kwargs) > 0:
			sys.stderr.write("ZeroWebSocket doesn't accept requests with both positional arguments and named arguments used.\n")
			return 2

		try:
			wrapper_key = Site.get_wrapperkey(config["data_directory"], site)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

		address = config.get("server.address", "127.0.0.1")
		port = config.get("server.port", "43110")
		secure = config.get("server.secure", False)

		with ZeroWebSocket(wrapper_key, "%s:%s" % (address, port), secure) as ws:
			try:
				print ws.send(cmd, *args, **kwargs)
				return 0
			except ZeroWebSocket.Error as e:
				sys.stderr.write("%s\n" % "\n".join(e))
				return 1


	def actionUser(self, *args, **kwargs):
		"""
			Configure users

			Subcommands:
			user list                   Get list of addresses
		"""

		raise Callable.SubCommand

	def actionUserList(self):
		"""
			Get list of addresses

			Usage:
			user list                   Print newline-separated list of addresses
		"""

		print "\n".join(User.get_users(config["data_directory"]))

try:
	sys.exit(ZeroNet(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)