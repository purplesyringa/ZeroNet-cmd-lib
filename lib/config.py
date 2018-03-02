import os, json

class Config(object):
	def __init__(self, path):
		self.__dict__["path"] = path

	# Read single value
	def __getattr__(self, name):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
				return config[name]
		except IOError:
			raise AttributeError("No config file and therefore no '%s' attribute" % name)

	# Read value recursively
	def get(self, name, default=None):
		name = name.split(".")

		try:
			val = self[name[0]]
			for part in name[1:]:
				val = val[part]

			return val
		except AttributeError:
			return default

	# Write single value
	def __setattr__(self, name, value):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		config[name] = value

		with open(self.path, "w") as f:
			f.write(json.dumps(config))

	# Write value recursively
	def set(self, name, value):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		current = config
		for part in name.split(".")[:-1]:
			try:
				current = current[name]
			except AttributeError:
				current[name] = dict()
				current = current[name]

		current[name] = value

		with open(self.path, "w") as f:
			f.write(json.dumps(config))

current_dir = os.path.dirname(os.path.abspath(__file__))
config_json = os.path.abspath(os.path.join(current_dir, "../config.json"))
config = Config(config_json)