#!/usr/bin/python2
import sys
import urllib2
import socket
import urllib
import os

threadurl=sys.argv[1]

#
print "Fetching images from",threadurl
f=urllib2.urlopen(threadurl,None,5)
site=f.read()
f.close()

print "Found",site.count("fileThumb"),"images."
imagesnum=site.count("fileThumb")
#Put split string at "fileThumb"
imagelines=site.split("fileThumb")[1:]

for i in range(len(imagelines)):
    indexstart=imagelines[i].index("href=")+8
    imagelines[i]= imagelines[i][indexstart:]
    indexend=imagelines[i].index('"')
    imagelines[i]="http://"+imagelines[i][:indexend]


#get thread number
threadnumstart=threadurl.index("thread/")+7
threadnum=threadurl[threadnumstart:]
for i in range(len(threadnum)):
    if not str(i) in ["1","2","3","4","5","6","7","8","9","0"]:
        print i
        threadend=i-1
        break
threadnum=threadnum[:threadend]
if "/" in threadnum:
    threadnum=threadnum[:threadnum.index("/")]

if not os.path.exists(threadnum):
    print "Creating directory",threadnum
    os.makedirs(threadnum)

for i in range(len(imagelines)):
    print "Downloading image",i+1,"out of",len(imagelines)
    urllib.urlretrieve(imagelines[i],threadnum+"/"+imagelines[i].split("/")[-1])
