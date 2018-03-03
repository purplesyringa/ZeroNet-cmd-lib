import json

def getWrapperkey(data_directory, address):
	with open("%s/sites.json" % data_directory) as f:
		sites = json.loads(f.read())
		if address in sites:
			return sites[address]["wrapper_key"]
		else:
			raise KeyError("No site %s" % address)

def findByWrapperkey(data_directory, wrapper_key):
	with open("%s/sites.json" % data_directory) as f:
		sites = json.loads(f.read())

		for address, site in sites.iteritems():
			if site["wrapper_key"] == wrapper_key:
				return address

		raise KeyError("No wrapper key %s" % wrapper_key)