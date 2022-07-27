import urllib
import urllib.request
import re
import os, sys

mb_url_t = 'https://www.metabolomicsworkbench.org/data/show_metabolites_by_study.php?STUDY_ID=ST002217&SEARCH_TYPE=KNOWN&STUDY_TYPE=MS&RESULT_TYPE=1'

def MetabolitesPage(mb_url_t):
    metabolitespage = urllib.request.urlopen(mb_url_t).read().decode('utf-8')
    return metabolitespage

def getAllMetabolites(metabolitespage):
    mb_regex = re.compile("MULTIPLE></td>[a-zA-Z0-9_()-±+',_\[\]α-ωΑ-Ω\s]*?</td>", re.DOTALL | re.M) #this is the best I can came up with so far that can find all metabolites
    mb_test = mb_regex.findall(metabolitespage)
    mb_test = [a.replace('MULTIPLE></td><td>', '') for a in mb_test]
    mb_test = [a.replace('</td>', '') for a in mb_test]
    return mb_test

#<input type="checkbox" name="fields[]" value="ME536959__(±)10(11)-EpDPA" multiple="">

def main(mb_url_t):
    metabolitespage = MetabolitesPage(mb_url_t)
    mb_test = getAllMetabolites(metabolitespage)
    t = open('All Metabolites.txt', 'w', encoding="utf-8")
    t.write('\n'.join(mb_test))
    t.close()
    return mb_test


t = main(mb_url_t)
print (t)
