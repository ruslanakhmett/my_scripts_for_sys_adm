import requests
import urllib3
import datetime
from time import sleep

urllib3.disable_warnings()


DOCS_MAX_LIMIT = 15000
BEEP_URL_METHOD_STRING = 'https://app.ru/api/v1/devices/mass-beep?'
today_now = datetime.datetime.today()


def get_token():
    try:
        gettok = requests.post('https://app.ru/api/v1/token',
        headers = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded', 'Accept': 'application/json, text/plain, */*'}, verify=False,
        data = 'grant_type=password&username=nameu&password=passwd')
        return gettok.json()['access_token']
    
    except Exception as err:
        with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                    file.write(f'{today_now}    Ошибка авторизации (get_token) {str(err)}\n')


def get_info():
    try:
        response = requests.get('https://app.ru/api/v1/devices?count=40000',
        headers= {'Authorization':'Bearer ' + get_token(), 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
        return response.json()
    
    except Exception as err:
        with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                    file.write(f'{today_now}    Ошибка при отправке запроса (get_info) {str(err)}\n')


def generate_kkt_id_array() -> list:
    try:
        target_kkt_array = []
        for item in get_info():
            if item['state']['fsDocumentsCount'] >= DOCS_MAX_LIMIT:
                target_kkt_array.append((item['id'], item['serialNumber'], item['comment']))
        return target_kkt_array
    
    except Exception as err:
        with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                    file.write(f'{today_now}    Ошибка обработки данных (generate_kkt_id_array) {str(err)}\n')


def send_beep(kkt_array: list):
    try:
        result_request_string = BEEP_URL_METHOD_STRING + '&'.join(['Devices=' + item[0] for item in kkt_array])
        response = requests.post(result_request_string, headers= {'Authorization':'Bearer ' + get_token(), 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)

    except Exception as err:
        with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                    file.write(f'{today_now}    Ошибка при отправке гудка (send_beep) {str(err)}\n')
    
    if response.status_code == 200:
        for item in response.json()['results']:
            for elem in kkt_array:
                if item['id'] == elem[0]:
                    with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                        file.write(f'{today_now}    {elem[1]} {elem[2].strip()} beep-> {item["isOk"]} \n')
    else:
        with open("/var/log/overfull_fn_beeper/overfull_fn_beeper.log", "a") as file:
                        file.write(f'{today_now}    Вернулся некорректный ответ {response.status_code} \n')


while True:
    
    send_beep(generate_kkt_id_array())
    sleep(1200)
