from clirender.layout.libs.library import Library, Slot

class ZeroFrame(object):
	def __init__(self, site, ws):
		self.site = site
		self.ws = ws

	def cmd(self, cmd):
		return self.ws.send(cmd)

def createLib(site, ws):
	cached = {}

	class ZeroFrameLib(Library):
		def __init__(self, layout):
			super(ZeroFrameLib, self).__init__(layout)

		@Slot("ZeroFrame", wrapped=True)
		def ZeroFrame(slots):
			return ZeroFrame(site, ws)

		@Slot("cached")
		def cached(fn, *args):
			if (fn, args) not in cached:
				cached[fn, args] = fn(*args)
			return cached[fn, args]

	return ZeroFrameLib