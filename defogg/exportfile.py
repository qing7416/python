# coding: utf-8
def ExportFile(path, file, content):
	path = path + '/' + file
	path = path.encode('utf-8')
	fnew = open(path, "w", encoding="utf-8")
	fnew.write(content)
	fnew.close()