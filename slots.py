import requests
from datetime import datetime

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

now = datetime.now()
today_date = now.strftime("16-06-2021")
api_url_telegram = "https://api.telegram.org/bot1735011715:AAHpjXDlsL2EybkbM58aM1Is2vMVKdmzego/sendMessage?chat_id=@__groupid__&text="
group_id = "slot_checker_cowin"

def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    final_url = base_cowin_url + query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
    print(response.text)


def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and  session["min_age_limit"] == 18:
                message = "Pincode: {}, \nName: {}, \nSlots: {}, \nMinimun Age: {}".format(
                  center["pincode"], center["name"], session["available_capacity_dose1"], session["min_age_limit"])
                send_message_telegram(message)




def send_message_telegram(message):  
    final_telegram_url = api_url_telegram.replace("__groupid__", group_id)     
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)  
    print(response)         

      
if __name__ == "__main__":
    fetch_data_from_cowin(670)  
