from readability.readability import Document
import urllib2
import re
import time
import os
from bs4 import BeautifulSoup

#NOTE: this is in python 2.7 and is the working version
#This file only needed to run once to crawl the archives for links


def writeToFile(link):
    #category = link.split('/')[3] # CATEGORY NAME
    #print(category + " : " + link)
    #print(os.getcwd())
    print(link)
    fo = open("links.txt", "a")
    fo.write(link + "\n")
    
def crawlGuardianArchives():
    categories = ("news", "sport", "culture", "business", "money", "lifeandstyle", "travel", "environment", "technology", "tv-and-radio")
    for i in categories:
        #time.sleep(10)
        for j in range(2, 31):
            if (j < 10):
                getGuardianArchivesLinks("http://www.theguardian.com/" + i + "/2014/apr/0" + str(j) + "/all")
            else:
                getGuardianArchivesLinks("http://www.theguardian.com/" + i + "/2014/apr/" + str(j) + "/all")


def getGuardianArchivesLinks(url):
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0' }
    req = urllib2.Request(url, '', headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    
    data = soup.findAll('div',attrs={'class':'trail'});
    for h3 in data:
        links = h3.findAll('a')
        for a in links:
            if a.parent.name  == "h3":
                writeToFile(a['href'])
                
        
def main():
    os.chdir("../../Corpus")
    #crawlGuardianArchives()  #THEY HAVE BEEN CRAWLED, NOW WORK WITH THE LINKS FILE
    
main();


