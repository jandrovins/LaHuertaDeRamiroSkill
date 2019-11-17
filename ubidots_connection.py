import requests
import time

API_KEY="BBFF-1fa452d00a15f98a01f33dc75ca142da083"
TOKEN="BBFF-L3aFxBtcfSkwg0DTnvk288WbYeB4fd"

DEVICE_LABEL="raspi"
url="http://industrial.api.ubidots.com"
url="{}/api/v1.6/devices/{}".format(url,DEVICE_LABEL)
headers= {"X-Auth-Token":TOKEN, "Content-Type": "application/json"}


def send_data(LABEL1,VARIABLE):
    LABEL=LABEL1
    
    payload = {LABEL:VARIABLE}
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)
        
    if status >= 400:
        print("ERROR: Could not send data after 5 attempts")
    else:
        print("INFO: request made properly")
        print("FINISHED")
        time.sleep(1)


