from readability.readability import Document
import urllib2
import re
import time
import os
from bs4 import BeautifulSoup

#NOTE: this is in python 2.7 and is the working version
#This file will only be needed to crawl articles and store them and their data as files

def removeTags(html, *tags):
    soup = BeautifulSoup(html)
    for tag in tags:
        for tag in soup.findAll(tag):
            tag.replaceWith("")
            
    return soup

def getArticleInfo(url):
    #headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0' }
    
    try:
        req = urllib2.Request(url)
        html = urllib2.urlopen(req).read()
    except urllib2.URLError:
                print("Unable to open previous article. URLError")
                return False
    articleWithHTML = Document(html).summary()
    title = Document(html).short_title()
    retArr = (title, articleWithHTML)
    return retArr

def getArticleHeadings(articleWithHTML):
    for heading in articleWithHTML.find_all('h2'):
        print(heading)

def cleantags(article):
    article = removeTags(article, 'pre')
    article = str(article)
    article = re.sub('<[^>]*>', '', article)
    article = re.sub('&#13;', '', article)
    return article   

def analyzeArticlesFromList():
    fo = open("links.txt", "r")
    os.chdir("docs/testing/")
    print(os.getcwd())
    with fo as f:
      for line in f:
        #print(line),  
        category = line.split('/')[3] # CATEGORY NAME
        if (category == "sport"):
            articleInfo = getArticleInfo(line)
            
            if (articleInfo is False):
                continue
            print(articleInfo[0])
            try :
                fw = open("sport/" + articleInfo[0] + ".txt", "w")
            except IOError, e:
                print("Unable to open previous article. IOError. %s" % e)
                continue
            
            fw.write(category + "\n \n")
            rawarticle = articleInfo[1]
            article = cleantags(articleInfo[1])
            fw.write(article)
            time.sleep(1)
            
        
def main():
    
    analyzeArticlesFromList()
    #articleInfo = getArticleInfo("http://www.theguardian.com/football/picture/2014/apr/01/footballviolence-photography")
    #title = articleInfo[0]
    #rawarticle = articleInfo[1]
    #article = cleantags(articleInfo[1])
    #soup = BeautifulSoup(rawarticle)
    #getArticleHeadings(soup)
    #print(title)
    #print(article)
    
main()


