#!/usr/bin/python2
import sys
import urllib2
import socket
import urllib
import os

def FetchThreads(Boardurl,boardname):
    print Boardurl
    f=urllib2.urlopen(Boardurl,None,5)
    site=f.read()
    f.close()
    sitesplit=site.split('<span class="subject">')[1:]
    newsitesplit=[]
    for i in range(len(sitesplit)):
        if i%2==0:
            newsitesplit.append(sitesplit[i])
    sitesplit=newsitesplit
    for i in range(len(sitesplit)):
        startindex=sitesplit[i].index('<a href="thread/')+16
        sitesplit[i]=sitesplit[i][startindex:]
        endindex=sitesplit[i].index('"')
        sitesplit[i]=sitesplit[i][:endindex]
        sitesplit[i]="http://boards.4chan.org/"+boardname+"/thread/"+sitesplit[i]
    return sitesplit

def FetchThread(url): #Return list of image urls for this thread
    f=urllib2.urlopen(url,None,5)
    site=f.read()
    f.close()
    imagelines=site.split("fileThumb")[1:]

    for i in range(len(imagelines)):
        indexstart=imagelines[i].index("href=")+8
        imagelines[i]= imagelines[i][indexstart:]
        indexend=imagelines[i].index('"')
        imagelines[i]="http://"+imagelines[i][:indexend]
    return imagelines

def GrabImages(imagelist,savepath): #Grab images in imagelist and save the to savepath
    if not os.path.exists(savepath):
        print "Creating directory",savepath
        os.makedirs(savepath)

    for i in range(len(imagelist)):
        print "Downloading image",i+1,"out of",len(imagelist)
        urllib.urlretrieve(imagelist[i],savepath+"/"+imagelist[i].split("/")[-1])
    return 0

if "-b" == sys.argv[1]: #Fetch an entire board
    
    boardurl=sys.argv[2]
    if len(sys.argv)>3:
        pagenum=int(sys.argv[3])
        if pagenum>10:
            pagenum=10
    else:
        pagenum=1
    #fect board url (name after 4chan.org/)
    boardname=boardurl[boardurl.index("4chan.org/")+10:]
    if "/" in boardname:
        boardname=boardname[:boardname.index("/")]
    Threads=[]
    if "-R" in sys.argv:
        for i in range(1,pagenum+1):
            if i==1:
                Threads+=FetchThreads("http://boards.4chan.org/"+boardname+"/",boardname)
            else:
                Threads+=FetchThreads("http://boards.4chan.org/"+boardname+"/"+str(i),boardname)
    else:
        if pagenum==1:
            Threads+=FetchThreads("http://boards.4chan.org/"+boardname+"/",boardname)
        else:
            Threads+=FetchThreads("http://boards.4chan.org/"+boardname+"/"+str(pagenum),boardname)
    images=[]
    for i in range(len(Threads)):
        print "Searched",i,"threads out of",len(Threads),len(images), "images found so far"
        images+=FetchThread(Threads[i])
    print"Found a total of",len(images),"images!."
    if len(images)>500:
        print "Fetching. This probably gonna take a long time"
    else:
        print "Fetching."
    GrabImages(images,boardname)
    
    sys.exit(0)
    

else:
    threadurl=sys.argv[1]
    print "Fetching images from",threadurl
    images=FetchThread(threadurl)
    print "Found",len(images),"images."
    if not len(images)==0:
        #get thread number
        threadnumstart=threadurl.index("thread/")+7
        threadnum=threadurl[threadnumstart:]
        for i in range(len(threadnum)):
            if not str(i) in ["1","2","3","4","5","6","7","8","9","0"]:
                threadend=i-1
                break
        threadnum=threadnum[:threadend]
        if "/" in threadnum:
            threadnum=threadnum[:threadnum.index("/")]
        GrabImages(images,threadnum)

