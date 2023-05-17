import time
import requests
import json
import csv

OUTPUT_PATH = './data/wunderground.csv'

def month_days(year,month):
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        return 31
    elif (month == 4 or month == 6 or month == 9 or month == 11):
        return 30
    elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
        return 29
    else:
        return 28
url='https://api.weather.com/v1/location/KMDW:9:US/observations/historical.json?'

with open(OUTPUT_PATH,'w',newline='') as fp:
    csvwrite=csv.DictWriter(fp,fieldnames=['Date','Time','Temperature','Dew Point',
                                           'Humidity','Wind','Wind Speed','Wind Gust',
                                            'Pressure','Precip','Condition',])
    csvwrite.writeheader()
    for month in range(1,13):
        days=month_days(2022,month)
        if month<10:
            month='0'+str(month)
        params={
        'apiKey': 'e1f10a1e78da46f5b10a1e78da96f525',
        'units': 'e',
        'startDate': '2022'+str(month)+'1',
        'endDate': '2022'+str(month)+str(days),
        }
        response0=requests.get(url=url,params=params)
        print(response0)
        response1=response0.text
        response1=json.loads(response1)
        response1=response1['observations']

        for i in range(len(response1)):
            dic0=response1[i]
            s_time2=time.localtime(dic0["valid_time_gmt"]-13*3600)
            time1=time.strftime("%Y-%m-%d", s_time2)
            time2=time.strftime("%H:%M:%S", s_time2)
            print(time1)
            dic={}
            dic['Date']=time1
            dic['Time']=time2
            dic['Temperature']=dic0['temp']
            dic['Dew Point']=dic0['dewPt']
            dic['Humidity']=dic0['rh']
            dic['Wind']=dic0['wdir_cardinal']
            dic['Wind Speed']=dic0['wspd']
            dic['Wind Gust']=dic0['gust']
            dic['Pressure']=dic0['pressure']
            dic['Precip']=dic0['precip_hrly']
            dic['Condition']=dic0['wx_phrase']
            print(dic)
            csvwrite.writerow(dic)
            
            #When the csv file is downloaded, the time interval in the csv file is not fixed, and the granularity of the hourly weather data is better according to the requirements, so you can open the file and filter the time in excel: just select all the times that contain 53
