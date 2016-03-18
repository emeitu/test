

i=50
j=12

d1=44.0
d2=11.3

#print d1/j
##print d1//d2
print "name:%s, age:%d" % ('dada',13)


print 2**3

name="mingqi"

print name[-1];

print name*2

try:
	fileName=raw_input("Enter file name:")
	fobj = open(fileName, 'r')
	for eachLine in fobj:
		print eachLine
	fobj.close();
except IOError, e:
	print 'file open err:',e

	
age="1213"
print "age:",age
age=26
print age



#for item in ["e-mail${name}", 'net-surfing', 'homework']:
#	print item
#
#who='ming'
#what='Ni!'
#print 'We are the', who, 'who say',what,what,what 


for i in range(1,3) :
    print i

print i
