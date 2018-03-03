import psutil, os

def isRunning(data_directory):
	try:
		with open("%s/lock.pid" % data_directory, "w") as f:
			f.write("0")
			return True
	except IOError:
		return False


def getPid(data_directory):
	lock_file = os.path.realpath("%s/lock.pid" % data_directory).encode("utf-8")

	for proc in psutil.process_iter():
		try:
			if lock_file in (x.path for x in proc.open_files()):
				return proc.pid
		except psutil.Error as e:
			pass

	return None