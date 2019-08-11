###Script for scraping transaction statistics from Estonian Land Board - http://www.maaamet.ee/kinnisvara/htraru
###Currently outputs JSON files for each report, which have to be processed further. 
###Session data should be regenerated for each client.
###USAGE: python htraru.py YEAR EHAK_CODE
from lxml import html
import requests
import sys
aasta = int((sys.argv[1]))
 
cookies = {
    'has_js': '1',
    'ASP.NET_SessionId': 'RENEW_THIS',
}

headers = {
    'User-Agent': 'SCRAPER: https://github.com/okestonia/opendata-issue-tracker/issues/218 for more information',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'http://www.maaamet.ee/kinnisvara/htraru/Start.aspx',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

from datetime import date, datetime, timedelta

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta
		
### T01 Tehingud tehinguliikide kaupa
### T02 Tehingud võõrandajate järgi
### T03 Tehingud omandajate järgi
### T04 Kinnisasja tehingud sihtotstarvete järgi
### T05 Kinnisasja tehingud kinnistu osade kaupa
### T06 Tehingud kuude lõikes
### T14 Tehingud objekti liigi järgi
### T08 Tehingud maakondade kaupa
### R01 Tehingud võõrandajate residentsuse kaupa
### R02 Tehingud omandajate residentsuse kaupa

reports = ['T01', 'T02', 'T03', 'T04', 'T05', 'T14', 'R01', 'R02']
      
data = {
  'RBLLang': 'et',
  'DDTrykis': 'D',
  'RBLTehingud': '0',
  'LBTrykis': 'T06',
  'chkYksPiirkond': 'on',
  'txtAlgus': '01.01.2008',
  'txtLopp': '01.01.2019',
  'RBLAeg': '0',
  'btnTryki': 'Koosta aruanne',
  'INFOTEXT': '',
  'TRYKIS': '',
  'TRTYYP': '',
  'TEHINGU_LIIK': '',
  'HEADER': '',
  'HEADER1': '',
  'HEADER2': '',
  'MARKUS': '',
  'VARJANIMI': '',
  'VARJAKP': '',
  'PARAMS': '',
  'TULEM': '',
  'INADS_EHAK': '0037',
  'INADS_AADRESS': 'TEST FOR SCRAPING',
  '__EVENTTARGET': '',
  '__EVENTARGUMENT': '',
  '__LASTFOCUS': '',
  '__VIEWSTATE': 'RENEW_THIS'}


#ehaklist = ['A108', 'A409', 'A404', 'A207', 'A314', 'A407', 'A307']
ehaklist = [(sys.argv[2])]
for report in reports:

    for ehakcode in ehaklist:
        for day in datespan(date(aasta, 1, 1), date(aasta, 12, 31), delta=timedelta(weeks=1)):
            print (day, day + timedelta(days=6))
            data['INADS_EHAK'] = ehakcode
            data['LBTrykis'] = report
            data['txtAlgus'] = day
            data['txtLopp'] = day + timedelta(days=6)
			

            response = requests.post('http://www.maaamet.ee/kinnisvara/htraru/FilterUI.aspx', headers=headers, cookies=cookies, data=data)
            tree = html.fromstring(response.content)
            
            tulem = tree.xpath('//input[@name="TULEM"]/@value')

            try:
                if len(tulem[0])>10:
                    with open("logs/" + ehakcode  + "_" + report + "_" + str(data['txtAlgus']) + "_" + str(data['txtLopp']) + ".json", "w") as ff:
                        print (tulem[0], file=ff)
 
            except:
                print ("failed: " + ehakcode  + " " + report + " " + str(data['txtAlgus']) + " " + str(data['txtLopp']))
                print (response.text)

