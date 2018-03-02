import sys

class Callable(object):
	def __init__(self, cmd, args):
		try:
			handler = getattr(self, "action" + cmd[0].upper() + cmd[1:])
		except AttributeError:
			all_commands = [name[6].lower() + name[7:] for name in dir(self) if name.startswith("action")]
			sys.stderr.write("Unknown command %s. Allowed commands are: %s\n" % (cmd, ", ".join(all_commands)))
			return

		if self.checkCall(cmd, handler, args):
			handler(*args)

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