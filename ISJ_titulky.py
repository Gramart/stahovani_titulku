#
# ISJ - Project, Automaticke stahovani a srovnavani titulku k filmum
# Copyright Martin Graca, BUT, 1BIA
# April 2014

import urllib
import re
import sys
import json
import zipfile
import os
import glob
import codecs
from datetime import timedelta # pro praci s casem titulku
from xml.etree.ElementTree import iterparse
import datetime
print datetime.timedelta(0, 115, 259000)
print datetime.timedelta(0, 114, 157000)
Imdb_file = urllib.urlopen('http://www.omdbapi.com/?i=&t=the+mist')

data = json.loads(Imdb_file.read()) # ulozeni KB z omdbapi.com
Imdb_file.close()
#print data['imdbID']

#fobj = urllib.urlopen('http://www.opensubtitles.org/cs/search/sublanguageid-all/imdbid-0884328/xml')
#fobj = urllib.urlopen('http://www.opensubtitles.com/cs/subtitles/3258272/the-mist-cs/xml')
fobj = urllib.urlopen('http://www.opensubtitles.org/cs/subtitles/4873857/the-mist-cs/xml')
czefile = open('cze_movie.xml','w')
czefile.write(fobj.read())
fobj.close()
czefile.close()
readfile = open('cze_movie.xml', 'r')

readfile.close()


with open('cze_movie.xml', 'r') as f: #, encoding='utf-8') as f:
    for event, elem in iterparse(f):
            if elem.find("Download") is not None:
                LinkDownload = elem.find("Download").attrib['LinkDownload']
            if elem.find("MovieName") is not None:
                MovieID = elem.find("MovieName").attrib['MovieID'] # najde ID filmu na opensubtitles
            
print MovieID
print LinkDownload

file_obj = urllib.urlopen('http://www.opensubtitles.org/en/search/sublanguageid-eng/idmovie-'+MovieID+'/xml')
eng_file = open('eng_movie.xml','w')
eng_file.write(file_obj.read())
file_obj.close()
eng_file.close()
EnLinkDownload = []
if EnLinkDownload:
        print 'plny'
else:
        print 'prazdny'

        
with open('eng_movie.xml', 'r') as f: #, encoding='utf-8') as f:
    for event, elem in iterparse(f):
        if elem.tag == 'subtitle':
            if elem.find("IDSubtitle") is not None:
                EnLinkDownload.append(elem.find("IDSubtitle").attrib['LinkDownload'])
            if elem.find("SubSize") is not None:
                EnLinkDownload.append(elem.find("SubSize").text)


print "downloading cz subtitles..."
def download_sub(LinkDownload):
  if not os.path.exists('cz/'):
            os.makedirs('cz/')
  urllib.urlretrieve(LinkDownload, "cz/cz_titulky.zip")

        
cz_zip_soubor = zipfile.ZipFile('cz/cz_titulky.zip', 'r')
for n in cz_zip_soubor.namelist():
    if '.nfo' not in n:
        if not os.path.exists('cz/cz_titulky'):
            os.makedirs('cz/cz_titulky')
        open('cz/cz_titulky/'+n, 'w').write(cz_zip_soubor.read(n))


# rozdeleni cz titulku do skupin
cz_groups = []
pole = []
for n in os.listdir("cz/cz_titulky"): # spoji vice DVD dohromady
  if '.nfo' not in n:
      with open('cz/cz_titulky/'+n, 'r') as Subtitles:
          splits = [s.strip() for s in re.split(r'\n\s*\n', Subtitles.read()) if s.strip()]
          regex = re.compile(r'''(?P<index>\d+).*?(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})\s*.*?\s*(?P<text>.*)''', re.DOTALL)
          for s in splits:
              r = regex.search(s)
              cztime = r.groups()[1].replace(',','.').split(':')
              cztime_do = r.groups()[2].replace(',','.').split(':')
              cz_time_od = timedelta(hours=int(cztime[0]),minutes=int(cztime[1]),seconds=float(cztime[2]))
              cz_time_do = timedelta(hours=int(cztime_do[0]),minutes=int(cztime_do[1]),seconds=float(cztime_do[2]))
              pole.append(r.groups()[0])
              pole.append(cz_time_od)
              pole.append(cz_time_do)
              pole.append(r.groups()[3])
              cz_groups.append(pole)
              pole = []
# uz tady prevest cas typu string na timedelta

print len(cz_groups)
en_groups = []
print os.listdir("cz/cz_titulky")


# rozdeleni en titulku do skupin
all_en_groups = []
pole = list()
for i in range(20): #range(l):    
    for n in os.listdir("en/en_titulky"+str(i)): # spoji vice DVD dohromady

        with open('en/en_titulky'+str(i)+'/'+n, 'r') as Subtitles:
          splits = [s.strip() for s in re.split(r'\n\s*\n', Subtitles.read()) if s.strip()]
          regex = re.compile(r'''(?P<index>\d+).*?(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})\s*.*?\s*(?P<text>.*)''', re.DOTALL)
          for s in splits:
              r = regex.search(s)
              entime = r.groups()[1].replace(',','.').split(':')
              entime_do = r.groups()[2].replace(',','.').split(':')
              en_time_od = timedelta(hours=int(entime[0]),minutes=int(entime[1]),seconds=float(entime[2]))
              en_time_do = timedelta(hours=int(entime_do[0]),minutes=int(entime_do[1]),seconds=float(entime_do[2]))
              pole.append(r.groups()[0])
              pole.append(en_time_od)
              pole.append(en_time_do)
              pole.append(r.groups()[3])
              en_groups.append(pole)
              pole = []
    all_en_groups.append(en_groups)
    en_groups = []
                          
    

out_file = open('out.txt', 'a')
print 'delka cz:'
print len(cz_groups)

# prirazeni titulku
print "prvni a druhy"
print len(all_en_groups[0])
print len(all_en_groups[1])
pole = []
prirad = {}
speach = []
for pocet in range(len(all_en_groups)):
  counter = 0
  print 'next'
  if pocet == 2:
### zacatek prirazovani titulku
    for i in range(len(cz_groups)):

        spojeni_vice_en_promluv = ''
        spojeni_vice_cz_promluv = ''
        doba_trvani_cz = cz_groups[i][2]-cz_groups[i][1]
        match = ''
		
        for l in range(len(all_en_groups[pocet])):
            doba_trvani_en = all_en_groups[pocet][l][2]-all_en_groups[pocet][l][1]
            rozdil_od = cz_groups[i][1] - all_en_groups[pocet][l][1]
            rozdil_do = cz_groups[i][2] - all_en_groups[pocet][l][2]

            if rozdil_od < timedelta(seconds=0):
                rozdil_od =  timedelta(days = -1,hours=24) - rozdil_od
            if rozdil_do < timedelta(seconds=0):
                rozdil_do = timedelta(days = -1,hours=24) - rozdil_do
            #print rozdil_do
            if (doba_trvani_cz - doba_trvani_en) < timedelta(seconds=0):      
                rozdil_trvani = timedelta(days = -1,hours=24) - (doba_trvani_cz - doba_trvani_en)
            else:
                rozdil_trvani = doba_trvani_cz - doba_trvani_en
            ''' spojeni vice en promluv '''
            if (rozdil_od < timedelta(seconds=1) and doba_trvani_en < doba_trvani_cz) or (rozdil_do < timedelta(seconds=1) and doba_trvani_en < doba_trvani_cz) or \
               (cz_time_od < en_time_od and en_time_do < cz_time_do and doba_trvani_en < doba_trvani_cz):
                if spojeni_vice_en_promluv is '':
                    spojeni_vice_en_promluv = all_en_groups[pocet][l][3] + ' '
                    pole.append(l)
                else:
                    spojeni_vice_en_promluv = (spojeni_vice_en_promluv + all_en_groups[pocet][l][3]).replace('\n',' ').replace('\r',' ')
                    pole.append(l)
            elif rozdil_od < timedelta(seconds=0.5):
                pole.append(l)
                match = str(all_en_groups[pocet][l][3])

#################################################################

        if spojeni_vice_en_promluv is not '':
            counter = counter + 1
            #print 'spojeni'
            prirad[i] = spojeni_vice_en_promluv.replace('\n',' ').replace('\r',' ')
        elif match is not '':
            prirad[i] = match.replace('\n',' ').replace('\r',' ')

            counter = counter + 1
        else:
            prirad[i] = ''              

    print 'len en groups:'
    print len(all_en_groups[pocet])
    print 'counter: '+str(counter)+'\n'
    procento_shody = counter*100/len(cz_groups)

    print 'Shoda',procento_shody,'%'
    
    for i in range(len(cz_groups)):
                out_file.writelines(cz_groups[i][3].replace('\n', ' ').replace('\r',' ')+'\t'+prirad[i]+'\n')
                if i not in pole and i < len(all_en_groups[pocet]):
                   out_file.writelines('\t'+str(all_en_groups[pocet][i][3]+'\n'))
out_file.close()
 
print 'done'
