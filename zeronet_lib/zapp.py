from __future__ import division

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

		@Slot("toColor")
		def toColor(text, saturation=30, lightness=50):
			import colorsys

			hashed = 0
			for pos, char in enumerate(list(text)):
				hashed += ord(char) * pos
				hashed %= 1777

			rgb = colorsys.hsv_to_rgb(hashed % 360 / 360, saturation / 100, lightness / 100)
			r, g, b = map(lambda part: hex(int(part * 255))[2:].zfill(2), rgb)
			return "#%s%s%s" % (r, g, b)

	return ZeroFrameLib