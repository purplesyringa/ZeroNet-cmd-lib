#!/usr/bin/env python

import sys, os
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.user as User
import zeronet_lib.instance as Instance
from zeronet_lib.zerowebsocket import ZeroWebSocket

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		config                      Get or set config values
		wrapperkey                  Return wrapper key of a site or find a site by wrapper key
		socket                      Send request to ZeroWebSocket
		account                     Configure accounts
		certs                       Configure certificates
		instance                    Get info about ZeroNet instance

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
				print Site.getWrapperkey(config["data_directory"], search)
			else:
				print Site.findByWrapperkey(config["data_directory"], search)
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
			wrapper_key = Site.getWrapperkey(config["data_directory"], site)
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


	def actionAccount(self, *args, **kwargs):
		"""
			Configure accounts

			Subcommands:
			account list                Get list of addresses
			account master              Get master_seed of account
			account choose              Choose account for actions
		"""

		raise Callable.SubCommand

	def actionAccountList(self):
		"""
			Get list of addresses

			Usage:
			account list                Print newline-separated list of addresses
		"""

		print "\n".join(User.getUsers(config["data_directory"]))

	def actionAccountMaster(self):
		"""
			Get master_seed of account

			Usage:
			account master              Print master_seed of current account
		"""

		address = self.getCurrentAccount()

		try:
			print User.getUser(config["data_directory"], address)["master_seed"]
		except KeyError:
			sys.stderr.write("No account %s\n" % address)
			return 1

	def getCurrentAccount(self):
		address = config.get("account.current", None)

		if address is None:
			address = User.getUsers(config["data_directory"])[0]
			config.set("account.current", address)

		return address
	def getCurrentUser(self):
		return User.getUser(config["data_directory"], self.getCurrentAccount())

	def actionAccountChoose(self, address):
		"""
			Choose account for actions

			Usage:
			account choose <address>    Use <address> account for all actions
		"""

		try:
			User.getUser(config["data_directory"], address)
		except KeyError:
			sys.stderr.write("No account %s\n" % address)
			return 1

		config.set("account.current", address)

	def actionCerts(self, *args, **kwargs):
		"""
			Configure certificates

			Subcommands:
			certs list                  Get list of certs
			certs address               Get auth_address of a cert
			certs privatekey            Get auth_privatekey of a cert
			certs username              Get user name of a cert
		"""

		raise Callable.SubCommand

	def actionCertsList(self):
		"""
			Get list of certs

			Usage:
			certs list                  Print newline-separated names of auth certs
		"""

		print "\n".join(self.getCurrentUser()["certs"].keys())

	def actionCertsAddress(self, cert):
		"""
			Get auth_address of a cert

			Usage:
			certs address <cert>        Print auth_address of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_address"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1

	def actionCertsPrivatekey(self, cert):
		"""
			Get auth_privatekey of a cert

			Usage:
			certs privatekey <cert>     Print auth_privatekey of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_privatekey"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1

	def actionCertsUsername(self, cert):
		"""
			Get user name of a cert

			Usage:
			certs username <cert>       Print auth_user_name of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_user_name"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1


	def actionInstance(self, *args, **kwargs):
		"""
			Get info about ZeroNet instance

			Subcommands:
			instance running            Check whether ZeroNet instance is running
			instance pid                Get PID of ZeroNet instance
		"""

		raise Callable.SubCommand

	def actionInstanceRunning(self):
		"""
			Check whether ZeroNet instance is running

			Usage:
			instance running            Return 0 if running, 1 otherwise
		"""

		return 1 if Instance.isRunning(config["data_directory"]) else 0

	def actionInstancePid(self):
		"""
			Get PID of ZeroNet instance

			Usage:
			instance pid                Return 0 and print the PID if running, return 1 otherwise
		"""

		pid = Instance.getPid(config["data_directory"])
		if pid is None:
			return 1
		else:
			print pid
			return 0

try:
	sys.exit(ZeroNet(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)