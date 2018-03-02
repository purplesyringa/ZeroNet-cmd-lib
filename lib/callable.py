import sys, inspect

class Callable(object):
	class SubCommand(Exception):
		pass
	class Redirect(Exception):
		pass

	def __init__(self, args):
		self.call("", args)

	def call(self, cmd, args):
		cmd = cmd.strip()

		try:
			handler = getattr(self, "action" + "".join(map(lambda part: part[0].upper() + part[1:] if part != "" else "", cmd.split(" "))))
		except AttributeError:
			all_commands = [name[6].lower() + name[7:] for name in dir(self) if name.startswith("action") and len(name) > 6]
			sys.stderr.write("Unknown command '%s'. Allowed commands are: %s\n" % (cmd, ", ".join(all_commands)))
			return

		if self.checkCall(cmd, handler, args):
			try:
				self.callArgs(handler, args)
			except Callable.SubCommand as e:
				if len(args) == 0:
					sys.stderr.write("'%s' command is not a command but has subcommands.\n" % cmd)
					return
				self.call("%s %s" % (cmd, args[0]), args[1:])
			except Callable.Redirect as e:
				if len(tuple(e)) == 0:
					# Remove first argument and call it (as SubCommand)
					if len(args) == 0:
						sys.stderr.write("'%s' command is not a command but has subcommands.\n" % cmd)
						return
					self.call("%s %s" % (cmd, args[0]), args[1:])
				elif len(tuple(e)) == 1:
					# Call given value
					self.call(tuple(e)[0], args)
				else:
					# Call given value and arguments
					self.call(tuple(e)[0], tuple(e)[1])

	def checkCall(self, cmd, func, args):
		import inspect

		expected_args = inspect.getargspec(func).args[1:] # Split "self"
		varargs = inspect.getargspec(func).varargs
		defaults = inspect.getargspec(func).defaults or tuple()

		if varargs is not None:
			if len(args) >= len(expected_args) - len(defaults):
				return True
		else:
			if len(expected_args) - len(defaults) <= len(args) <= len(expected_args):
				return True

		if varargs is not None:
			sys.stderr.write("%s expected %s argument(s) or more, %s given\n" % (cmd, len(expected_args), len(args)))
			expected_args += ["*%s" % varargs]
		elif len(defaults) > 0:
			sys.stderr.write("%s expected from %s to %s argument(s), %s given\n" % (cmd, len(expected_args) - len(defaults), len(expected_args), len(args)))
		else:
			sys.stderr.write("%s expected %s argument(s), %s given\n" % (cmd, len(expected_args), len(args)))

		if len(defaults) > 0:
			default_args = reversed(zip(reversed(expected_args), reversed(defaults)))
			default_args = map(lambda arg: "%s=%s" % arg, default_args)
			expected_args = expected_args[:-len(default_args)] + default_args

		sys.stderr.write("Arguments: %s\n" % ", ".join(expected_args))

		return False

	def callArgs(self, handler, args):
		handler(*args)

	def action(self, *args):
		raise Callable.SubCommand

class WithHelp(Callable):
	def actionHelp(self, *cmd):
		if cmd in [[], [""], tuple(), ("",)]:
			# Print info about the class
			print inspect.cleandoc(self.__doc__)
			return

		try:
			handler = getattr(self, "action" + "".join(map(lambda part: part[0].upper() + part[1:], cmd)))
			if handler.__doc__ is not None:
				print inspect.cleandoc(handler.__doc__)
				return
		except AttributeError:
			pass

		if cmd == ["help"] or cmd == ("help",):
			# Unable to find info on topic 'help' - no __doc__ in 'help' method or no 'help' method, use default help
			print inspect.cleandoc(self.__doc__)
			return

		print "Unknown topic '%s'" % " ".join(cmd)

Callable.WithHelp = WithHelp