import urllib
import urllib.request
import re
import os, sys
import pandas as pd

def getGsmHtml():
    mb_url = 'https://www.metabolomicsworkbench.org/data/DRCCStudySummary.php?Mode=StudySummary&SortBy=Study%20ID&AscDesc=desc&ResultsPerPage=5000'
    mb_html = urllib.request.urlopen(mb_url).read().decode('utf-8')
    #print('2') #this is just to make sure this part of the code ran
    return mb_html

def getStudyRow(mb_html):
    StudyRow_regex = re.compile('<tr class="odd"><td><[^<]+</a></td>\n<td>[^<]+</td>\n<td>[^<]+</td>\n<td>[^<]+</td>\n<td.*\n<td.*\n<td>[^<]+</td>\n<td>[0-9]+</td>|<tr class="even"><td><[^<]+</a></td>\n<td>[^<]+</td>\n<td>[^<]+</td>\n<td>[^<]+</td>\n<td.*\n<td.*\n<td>[^<]+</td>\n<td>[0-9]+</td>', re.DOTALL | re.M)
    StudyRow = StudyRow_regex.findall(mb_html)
    return StudyRow

def getElements(StudyRow):
    elements = []
    studyID = re.findall(r'ST[0-9]*</a></td>', StudyRow[0])
    for i in range(len(studyID) - 1):
        i1, i2 = studyID[i], studyID[i + 1]
        pos1, pos2 = StudyRow[0].index(i1), StudyRow[0].index(i2)
        String = StudyRow[0][pos1:pos2]
        element = String.split('</td>')
        element = element[:-2]
        element = [x.replace('</a>', '') for x in element]
        element = [x.replace('\n<td>', '') for x in element]
        element = [x.replace('\n<td nowrap>', '') for x in element]
        elements.append(element)
    return (elements)


def geturl(mb_html): #find url for each individual study's main page
    url_regex = re.compile('<td><a.*ST.*</a></td>')
    url = url_regex.findall(mb_html)
    url = [i.lstrip('<td><a href=').split('>ST')[0] for i in url]
    urlfront = 'https://www.metabolomicsworkbench.org/data/'
    url_t = [urlfront + x for x in url]
    return url_t

def getSampleSummary(url_t):
    x = 0
    sample_elements = []
    summary_elements = []
    for i in url_t:
        StudyPage_html = urllib.request.urlopen(i).read().decode('utf-8')
        print (i)
        SampleType_regex = re.compile(
            '<b>Sample Type:</b></td><td>[^\n<]+</td>',
            re.DOTALL | re.M)
        SampleType = SampleType_regex.findall(StudyPage_html)
        SampleType = [i.replace('<b>Sample Type:</b></td><td>', '') for i in SampleType]
        SampleType = [i.replace('</td>', '') for i in SampleType]
        print (SampleType)
        StudySummary_regex = re.compile('<span itemprop="description">[^\n<]+</span>')
        StudySummary = StudySummary_regex.findall(StudyPage_html)
        StudySummary = [i.replace('<span itemprop="description">', '') for i in StudySummary]
        StudySummary = [i.replace('</span>', '') for i in StudySummary]
        #print (StudySummary)
        sample_elements.append(SampleType)
        summary_elements.append(StudySummary)
        #x = x + 1
        #if x > 2:
        #    break
    return (sample_elements, summary_elements)


def main():
    mb_html = getGsmHtml()
    StudyRow = getStudyRow(mb_html)
    url_t = geturl(mb_html)
    (sample_elements, summary_elements) = getSampleSummary(url_t)
    elements = getElements(StudyRow)
#    print(len(studyID))
#    print(i1)
#    print(i2)
#    print(pos1)
#    print(pos2)
#    print(String)
    print(elements)
    output =pd.DataFrame(elements, columns=['Study ID', 'Study Title', 'Species', 'Institute', 'Analysis', 'Released Date', 'Version', 'Samples'])
    output['Sample Type'] = pd.Series(sample_elements)
    output['Study Summary'] = pd.Series(summary_elements)
    output.to_excel('Output.xlsx')
    print (3)
    #t = open('test.txt', 'w', encoding="utf-8")
    #t.write('\n'.join(StudyRow))
    #t.close()
    return(StudyRow, url_t, sample_elements, summary_elements)




main()
