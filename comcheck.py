from urllib2 import urlopen
import sys, os, string, time

def check(s):
	index = None;
	page = urlopen("http://www.checkdomain.com/cgi-bin/checkdomain.pl?domain=" + str(s) + ".com")
	site_text = page.read()
	index = 4823 + 4 * len(string.split(str(s), ".")[0])
	# check
	return site_text[index:index+15] == "still available"
	
def sanitize(s):
	s = s.replace("\n", "")
	exclude = set(string.punctuation)
	exclude.remove("-")
	exclude.add(" ")
	s = ''.join(ch for ch in s if ch not in exclude)
	return s

if len(sys.argv) > 2:
	print "Too many parameters!"
	sys.exit()

print "Welcome to comcheck, a domain (.com) availability checking script!\n--"

to_check = None
bulk_list = []
already = 0 

### Make a bulk list here if desired ###

# by default will look for a dict.txt file, and if found, use that as the bulk list

if os.path.exists('dict.txt'):
	f = open('dict.txt', 'r')
	for line in f:
		bulk_list.append(sanitize(line))
	print "Dictionary read (" + str(len(bulk_list)) + " entries)"
	f.close()
	if os.path.exists('last.txt'):
		lastf = open('last.txt', 'r')
		lindex = int(lastf.readline())
		bulk_list = bulk_list[lindex:]
		already = lindex # so when it exits again, it saves current progress
		print str(lindex) + " entries already handled, taking it from there (" + str(len(bulk_list)) + " left)"

### End bulk list code ###

if len(sys.argv) == 2 and sys.argv[1]:
	print "Checking " + sys.argv[1] + ".com"
	to_check = sys.argv[1]
elif len(bulk_list) == 0:
	to_check = raw_input("Desired domain (.com assumed)? ")
else:
	# check bulk!
	count = 0
	solid_count = 0
	length = len(bulk_list)
	try:
		# open file
		f = open('available.txt', 'w')
		
		for name in bulk_list:
			count += 1
			if check(name):
				solid_count += 1
				f.write(name + ".com\n")
				print "(" + str(count) + "/" + str(length) + ") " +  name + ".com is open!"
				time.sleep(0.1)
			else:
				print "(" + str(count) + "/" + str(length) + ")"
		print "\n" + str(count) + " of " + str(length) + " are available."
		f.close()
	except KeyboardInterrupt:
		lastf = open('last.txt', 'w')
		lastf.write(str(count + already))
		lastf.close()
		print "\n\nCurrent index saved to last.txt, will be resumed automatically. \nCatch you later."
	
if len(bulk_list) == 0 and check(to_check):
	print "YES, " + to_check + ".com is open!"
elif len(bulk_list) == 0:
	print "NO, " + to_check + ".com is not open, or something went wrong."