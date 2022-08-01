import urllib
import urllib.request
import re
import os, sys


def getGsmHtml():
    mb_url = 'https://www.metabolomicsworkbench.org/data/DRCCStudySummary.php?Mode=StudySummary&SortBy=Study%20ID&AscDesc=desc&ResultsPerPage=5000'
    mb_html = urllib.request.urlopen(mb_url).read().decode('utf-8')
    #print('2') #this is just to make sure this part of the code ran
    return mb_html



def getdownload(mb_html):       #download link for study
    download_regex = re.compile('nowrap><a.*Uploaded data')
    downloadlink = download_regex.findall(mb_html)
    downloadlink = [i.lstrip('nowrap><a href=').split('>Uploaded')[0] for i in downloadlink]
    dowbloadlinkfront = 'https://www.metabolomicsworkbench.org/'
    downloadlink_t = [dowbloadlinkfront + x for x in downloadlink]
    return downloadlink_t



def geturl(mb_html): #find url for each individual study's main page
    url_regex = re.compile('<td><a.*ST.*</a></td>')
    url = url_regex.findall(mb_html)
    url = [i.lstrip('<td><a href=').split('>ST')[0] for i in url]
    urlfront = 'https://www.metabolomicsworkbench.org/data/'
    url_t = [urlfront + x for x in url]
    return url_t



def getMetabolites_url(url_t):
    for a in url_t:
        mb_url_t = []
        StudyPage = urllib.request.urlopen(a).read().decode('utf-8')
        mb_regex = re.compile('<a href=show_metabolites_by_study.php?.*>Show named metabolites</a>')
        mb_url = mb_regex.findall(StudyPage)
        mb_url = [i.lstrip("<a href=").split(">Show named metabolites</a>")[0] for i in mb_url]
        urlfront = 'https://www.metabolomicsworkbench.org/data/'
        mb_url_0 = [urlfront + x for x in mb_url]
        #x = open('test.txt', 'w')
        #x.write('\n'.join(mb_url_t))
        #x.close()
        mb_url_t.append(mb_url_0)
    return (mb_url_t)

#def getMetabolites(mb_url_t):
#    for a in mb_url_t:
#        url = a
#        studyIDpattern = re.compile('ST[0-9]+')
#        studyID = studyIDpattern.findall(url)
#        #print(studyID)
#        metabolitespage = urllib.request.urlopen(i).read().decode('utf-8')
#        mb_regex = re.compile("MULTIPLE></td>[a-zA-Z0-9_()-±+',_\[\]α-ωΑ-Ω\s]*?</td>",re.DOTALL | re.M)  # this is the best I can came up with so far that can find all metabolites
#        mb_test = mb_regex.findall(metabolitespage)
#        mb_test = [i.lstrip('MULTIPLE></td><td>').split('</td>')[0] for i in mb_test]
#        filename = "%s.txt" % studyID
#        t = open(filename, 'w', encoding="utf-8")
#        t.write('\n'.join(mb_test))
#        return (mb_test)


def main():
    mb_html = getGsmHtml()
    url_t = geturl(mb_html)
    downloadlink_t = getdownload(mb_html)
    mb_url_t = getMetabolites_url(url_t)
    #mb_test = getMetabolites(mb_url_t)
    g = open('study_url.txt', 'w')
    g.write('\n'.join(url_t))
    g.close()
    h = open('download_link.txt', 'w')
    h.write('\n'.join(downloadlink_t))
    h.close()
    #print('3') #this is just to make sure this part of the code ran
    x = open('test.txt', 'w')
    for i in mb_url_t:
        x.write(i + '\n')
    x.close()
    return(url_t,downloadlink_t,mb_url_t)#,mb_test)

main()

