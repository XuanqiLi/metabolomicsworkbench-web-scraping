import urllib
import urllib.request
import re
import os, sys



def geturl(mb_html): #find url for each individual study's main page
    url_regex = re.compile('<td><a.*ST.*</a></td>')
    url = url_regex.findall(mb_html)
    url = [i.lstrip('<td><a href=').split('>ST')[0] for i in url]
    urlfront = 'https://www.metabolomicsworkbench.org/data/'
    url_t = [urlfront + x for x in url]
    return url_t

def getdownload(mb_html):       #download link for study
    download_regex = re.compile('nowrap><a.*Uploaded data')
    downloadlink = download_regex.findall(mb_html)
    downloadlink = [i.lstrip('nowrap><a href=').split('>Uploaded')[0] for i in downloadlink]
    dowbloadlinkfront = 'https://www.metabolomicsworkbench.org/'
    downloadlink_t = [dowbloadlinkfront + x for x in downloadlink]
    return downloadlink_t


def getGsmHtml():
    mb_url = 'https://www.metabolomicsworkbench.org/data/DRCCStudySummary.php?Mode=StudySummary&SortBy=Study%20ID&AscDesc=desc&ResultsPerPage=5000'
    mb_html = urllib.request.urlopen(mb_url).read().decode('utf-8')
    #print('2') #this is just to make sure this part of the code ran
    return mb_html

def main():
    mb_html = getGsmHtml()
    url_t = geturl(mb_html)
#    url = geturl(mb_html)
    downloadlink_t = getdownload(mb_html)
#    u = open('urlTailOnly.txt', 'w')
#    u.write('\n'.join(url))
#    u.close
    g = open('study_url.txt', 'w')
    g.write('\n'.join(url_t))
    g.close()
    h = open('download_link.txt', 'w')
    h.write('\n'.join(downloadlink_t))
    h.close()
    #print('3') #this is just to make sure this part of the code ran
    return(url_t,downloadlink_t)

main()

