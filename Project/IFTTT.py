import requests

LINE_event_name = 'msg01'
LINE_key = 'durIO4foYl_dZXqXNMDzwg'
LINE_URL='https://maker.ifttt.com/trigger/' + LINE_event_name + '/with/key/' + LINE_key

def send_msg(value1="", value2="", value3=""):
    r = requests.post(LINE_URL, 
        params={"value1": value1,
                "value2": value2,
                "value3": value3
            }
        )
    return r