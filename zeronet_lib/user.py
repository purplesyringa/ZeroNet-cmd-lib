import json

def get_users_json(data_directory):
	with open("%s/users.json" % data_directory) as f:
		return json.loads(f.read())

def get_users(data_directory):
	return get_users_json(data_directory).keys()