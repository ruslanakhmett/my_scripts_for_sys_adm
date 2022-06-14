import json
import requests
import urllib3
import datetime, time
urllib3.disable_warnings()

#берем год, месяц и день на данный момент в числовом фомрате
today = str(datetime.datetime.today()).split(' ')[0]
today_year = int(today.split('-')[0])
today_month = int(today.split('-')[1])
today_day = int(today.split('-')[2])

# get token
gettok = requests.post('url',
headers = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded', 'Accept': 'application/json, text/plain, */*'}, verify=False,
data = 'grant_type=password&username=name&password=passwd')
token =  gettok.json()['access_token']

#количество дней, ниже которого сработает блокировка
warning_time_days = 1
#количество документов, означающее окончание ФН и значит нужна блокировка
doc_block_count = 244000

while True:
    # get info
    response = requests.get('url',
    headers= {'Authorization':'Bearer ' + token, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
    rj = response.json()
    if response.status_code != 200:
        continue
    for item in rj:
        if item['state']['fsExpirationDate'] and item['blocked'] == False  and item['state']['fiscalizedAt'] != None:
            #берем год, месяц и день, стоящие на кассе в числовом фомрате
            date_of_end_fn = item['state']['fsExpirationDate'].split('T')[0]
            hour_of_end_fn = item['state']['fsExpirationDate'].split('T')[1].split(':')[1]
            year_of_end_fn = int(date_of_end_fn.split('-')[0])
            month_of_end_fn = int(date_of_end_fn.split('-')[1])
            day_of_end_fn = int(date_of_end_fn.split('-')[2])
            #вычисляем разницу между датами
            aa = datetime.date(year_of_end_fn, month_of_end_fn, day_of_end_fn)
            bb = datetime.date(today_year, today_month, today_day)
            count_days = str(aa-bb).split()[0]
            
            #проверяем количество оставшихся дней работы, и если необходимо, блокируем:
            if int(count_days) <= warning_time_days and item['blocked'] == False:
                result_string = date_of_end_fn + ';' + count_days + ';' + item['serialNumber'] + ';'  + str(datetime.datetime.now()) + ';' +  'blocked_for_date, ' 
                item['blocked'] = True
                response = requests.put('url', headers= {'Authorization':'Bearer ' + token, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False, data = json.dumps(item))
                if response.status_code != 200:
                    result_string =  date_of_end_fn + ';' +  count_days + ';' +  item['serialNumber'] + ';'  + str(datetime.datetime.now()) + ';' +  'blocked_for_date_error'
                #если касса удачно заблокирована, закрываем смену:
                else:
                    response3 = requests.get('url' + item['id'] + '/closeShift', headers= {'Authorization':'Bearer ' + token, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
                    if response3.status_code != 200:
                        result_string += 'ShiftClose Error'
                    else:
                        result_string += 'ShiftClose DONE'
                #пишем логи
                with open("/../kkt_blocker.log", "a") as file:
                    file.write(result_string + '\n')
                continue
            
            
            #проверяем количество обработанных чеков, и если оно приближается к лимиту, предупреждаем:
            elif item['state']['fsDocumentsCount'] >= doc_block_count and item['blocked'] == False:
                item['blocked'] = True
                result_string2 = str(item['state']['fsDocumentsCount'])  + ';' +  item['serialNumber'] + ';'  + str(datetime.datetime.now()) + ';' +  'blocked_for_doc, '
                response2 = requests.put('url', headers= {'Authorization':'Bearer ' + token, 'Content-type':'application/json', 'Accept': 'application/json'},
                verify=False, data = json.dumps(item))
                #пишем логи
                if response.status_code != 200:
                    result_string2 = str(item['state']['fsDocumentsCount']) + ';' +  item['serialNumber'] + ';'  + str(datetime.datetime.now()) + ';' +  'blocked_for_doc_error'
                #если касса удачно заблокирована, закрываем смену:
                else:
                    response2 = requests.get('url' + item['id'] + '/closeShift', headers= {'Authorization':'Bearer ' + token, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
                    result_string2 += 'ShiftClose DONE'
                with open("/.../kkt_blocker.log", "a") as file:
                    file.write(result_string2 + '\n')
    time.sleep(1200)
