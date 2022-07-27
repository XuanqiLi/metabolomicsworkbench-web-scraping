import urllib
import urllib.request
import re
import os, sys


url_t= 'https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST002217&StudyType=MS&ResultType=1'
#url given for testing before merging the codes

def readStudyPage(url_t):  #open the main page for study
    StudyPage = urllib.request.urlopen(url_t).read().decode('utf-8')
    return StudyPage

def getMetabolites_url(StudyPage): #find page that contains all metabolites appeared in study
    mb_regex = re.compile('<a href=show_metabolites_by_study.php?.*>Show named metabolites</a>')
    mb_url = mb_regex.findall(StudyPage)
    mb_url = [i.lstrip("<a href=").split(">Show named metabolites</a>")[0] for i in mb_url]
    urlfront = 'https://www.metabolomicsworkbench.org/data/'
    mb_url_t = [urlfront + x for x in mb_url]
    return mb_url_t

#def MetabolitesPage(mb_url_t):
    metabolitespage = urllib.request.urlopen(mb_url_t).read().decode('utf-8')
    return metabolitespage

#def getAllMetabolites(metabolitespage):
    mb_regex = re.compile('multiple.*DPA</td>')
    mb_test = mb_regex.findall(metabolitespage)
    return mb_test




def main(url_t):
    StudyPage = readStudyPage(url_t)
    mb_url_t = getMetabolites_url(StudyPage)
    #metabolitespage = MetabolitesPage(mb_url_t)
    #mb_test = getMetabolites_url(metabolitespage)
    print ('3')
    return (mb_url_t)


m, = main(url_t)
print(m)