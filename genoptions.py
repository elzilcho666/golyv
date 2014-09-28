months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
for x in xrange(0, 5):
	print "<option value='%s'></option>" % (str(x).zfill(2)) #months[x-1]