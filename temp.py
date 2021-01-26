import requests
from bs4 import BeautifulSoup
import re
import csv
import urllib
import os
import urllib.request
import datetime



def getTempData(station):

    URL = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=36&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num=' + station

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    pattern = "([0-9]*\.[0-9])|>([0-9][0-9][0-9][0-9])<"

    patterna = "or precise date unknown(?s).*"

    patternb = "(?s).*View a year of daily data"

    patternc = "[0-9]*\.?[0-9]"


    #print soup

    result = re.findall(patterna, str(soup))

    result3 = re.findall(patternb, str(result))

    result2 = re.findall(pattern, str(result3))

    result4 = re.findall(patternc, str(result2))

    #print result4

    ##years1 = re.findall(">([0-9][0-9][0-9][0-9])<", str(result3))
    ##
    ##temps = re.findall("[0-9]*\.[0-9]", str(result3))
    ##
    ##for i in range(0, len(years1)): 
    ##    years1[i] = int(years1[i]) 
    ##
    for i in range(0, len(result4)): 
        result4[i] = float(result4[i]) 


    #-------------------------

    years = []
    years1 = []
    temps = []

    x = 1850.0

    while x < currentYear-1:
        years.append(x)
        x = x + 1


    #print(result4)

    y = 0
    dp = -1

    for i in range(0, len(result4)):
        if i == len(result4) - 1:
            years1.append(result4[y])
            if dp == 11:
                temps.append(result4[i])
            else:
                temps.append("")
            dp = -1
            y = i
        if result4[i] != result4[y] + 1:
            dp = dp + 1
        else:
            years1.append(result4[y])
            if dp == 12:
                temps.append(result4[i-1])
            else:
                temps.append("")
            dp = -1
            y = i
        
        



    ##y = 0
    ##j = 1
    ##
    ##for i in range(0, len(years)):
    ##    if (years[i] == result4[y]):
    ##        years1.append(years[i])
    ##        while (result4[y+j] != years[i] + 1):
    ##            temps.append(result4[y+j])
    ##            j = j + 1
    ##        y = j
    ##    else:
    ##        years1.append(years[i])
    ##        temps.append("")
    ##    j = 1

    temps2 = []

    y = 0

    #print years
    #print years1

    if len(years1) == 0:
        return

    for i in range(0, len(years)):
        #print years[i] , years1[y]
        if years[i] != years1[y]:
            temps2.append("")
        else:
            temps2.append(temps[y])
            if years1[y] == years1[-1]:
                y = 0
            else:
                y = y + 1


    x = 0
    csvfile = 'WeatherData.csv'
    with open(csvfile, 'r') as fin, open('new_'+csvfile, 'w', newline='') as fout:
        reader = csv.reader(fin, lineterminator='\n')
        writer = csv.writer(fout, lineterminator='\n')
        if True:
            writer.writerow(next(reader) + [station])
        for row, val in zip(reader, temps2):
            writer.writerow(row + [temps2[x]])
            x = x + 1
            
    os.remove(csvfile) # not needed on unix
    os.rename('new_'+csvfile, csvfile)


#----------------------------------------

currentYear = datetime.datetime.now().year

try:
    os.remove('file.txt')
except:
    None

urllib.request.urlretrieve('ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/lists_by_element/alpha/alphaAUS_122.txt', 'file.txt')

with open('file.txt', 'r') as file:
    data = file.read()

pattern = "[ |\n] ([0-9][0-9][0-9][0-9]?[0-9]?[0-9])"

patternAWS = "(Y)\n|(N)\n| ( )\n"

result = re.findall(pattern, str(data))

AWS = re.findall(patternAWS, str(data))

AWS1 = []

for i in AWS:
    if i[0] == "Y":
        AWS1.append(True)
    elif i[1] == "N":
        AWS1.append(False)
    elif i[0] == "" and i[1] == "":
        AWS1.append(True)

column1 = []

x = 1850.0

while x < currentYear-1:
    column1.append(x)
    x = x + 1

try:
    os.remove('WeatherData.csv')
except:
    None

with open('WeatherData.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Year'])
    for val in column1:
        #print(val)
        writer.writerow([val])

x = 0

getAWS = False

for i in result:
    #if AWS1[x] == getAWS:
    getTempData(i)
    #x = x + 1
