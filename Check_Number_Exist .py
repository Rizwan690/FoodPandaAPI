import uvicorn
from fastapi import FastAPI
import requests
from random import  randint


app = FastAPI()
proxyDict = [
        {"http":"http:Your_Proxy"}
        ]

@app.get("/number/{phone}")


async def foodpanda(phone):

    if phone.startswith('COUNTRY_CODE'):
        filter_phone = phone[2:] # It will replace first two digits of your country code
    else:
        filter_phone = phone

    token = 'YOUR_ACCOUNT_TOKEN'

    url = "https://pk.fd-api.com/api/v5/customers?language_id=1"
    
    
    payload = "{\r\n    \"email\": \"YOUR EMAIL\",\r\n    \"first_name\": \"YOUR_NAME\",\r\n    \"last_name\": \"YOUR_LAST_NAME\",\r\n    \"mobile_country_code\": \"COUNTRYCODE\",\r\n    \"COUNTRY_CODE\": \""+str(filter_phone)+"\"\r\n}"
    headers = {
    'authority': 'pk.fd-api.com',
    'x-px-original-token': '3:873d304e970fe6c8aa682461cbf4023d03df3b8731c576ffd495f5566c6e5d5a:BDlpNbmJveOPdooXwoFVJ1wTZCEu3GvojScY2w7X83Ss+Ts8m9ukLzxwvAti18kr2jdftJQFz6zY55lpaBszOQ==:1000:F+3RuJ0OvHaNbnyqD2/2yZd29LHLoEOwno/xo9W9jsm8su/Td/7tbe79FAoCIe+eZiUM6+mh/haIBlojchmvdK/Hqeq0H9AARdzN8UVI16Pre/HKCKbjopTY/xhNZGvHdrE+qdbIyC02pWo263Z6V0NKfmTOMZl7OWbnxA3V4ub9jbkyYG4356Qr+wzGKUcNzEV3UQ3wPzBNDe1BFK6h0Q==',
    'x-px-authorization': '4',
    'x-px-bypass-reason': 'Error checking sdk enabled - general failure',
    'widevine-id': 'android.media.UnsupportedSchemeException: Failed to instantiate drm object.',
    'rts': '2021-09-03T12:19:19+0500',
    'ruid': '0.3663305668386201',
    'r-sig': 'x2ABpUfqa/nwqcd65kVJxccVUbLQvyu1pgsEVI8HpV4=',
    'app-build': '212187911',
    'app-version': '21.16.1',
    'cust-code': 'pk0q1mip',
    'eks': 'aq3mnp',
    'perseus-client-id': '1630652040686.302062398159590979.WO0pLYBPe1',
    'perseus-session-id': '1630652040686.552602989330185509.0QaLeLEJAG',
    'adjust-ad-id': 'de2ea6bbf95d8135cdb9e488cfa11f05',
    'x-pd-language-id': '1',
    'api-client-version': '5.0',
    'device-make': 'samsung',
    'device-model': 'SM-N976N',
    'device-id': 'be293b6a48877d457041d5acd8688695',
    'app-name': 'com.global.foodpanda.android',
    'app-flavor': 'foodpanda',
    'user-agent': 'Android-app-21.16.1(212187911)',
    'build-number': '212187911',
    'build-type': 'release',
    'platform': 'android',
    'platform-version': '25',
    'authorization': 'Bearer '+str(token),
    'content-type': 'application/json; charset=UTF-8',
    'accept-encoding': 'gzip',
    'x-fp-api-key': 'android',
    'em-request-identifier': '7affe46d-6c37-4d6b-84af-35f3c5d5c59d',
    'Cookie': '__cf_bm=rEVQriXeTTMuXQkgU.ufAzQe5unFUUEyeuAl_iIIZKU-1630662090-0-AfXoUoOEXyN+/0orzqb/2sIfjIoNKr4KM/3lKoLI4agJl8n7VVcyWRsJbJdYQaDUoTDyCtcJj7UK6hl8VmaQ6d0=; _pxhd=si0bG9jW2aMDHVdoo6QFaXXxKP9MmNC2ASLb2bViJn1KCqcCNvDufOsh-uMJIsQU9duYKDz-5gJ9SlQqQiWItg==:nbeII2IAY-iXcePgF3C/siyZISt8pHJDiMykdRtyVsX1GERBgONc4tMyB3VCVNTYUwi4kZ3qh3u3Y/9BXIaCIVqwgOA88p1O8tEh3jCokQo='
    }
    proxy = randint(0,len(proxyDict)-1)
    try:
        response = requests.request("PUT", url, headers=headers, data=payload,proxies=proxyDict[proxy])
        res_json = response.json() 
        if res_json:
            
            message = res_json.get('data').get('developer_message')
            if message == 'A customer with the mobile number +'+str(phone)+' already exists':
                try:
                    finaldict={"_id":phone,"message":str(message),"status":"User Exist on Food Panda"}
                    return finaldict

                except Exception as ex:
                    print('[-]  Issue while Insertion, Exception  ::  ' + str(ex) + "   ||   Phone  ::  " + str(phone))
             
            else:
                not_exsist_message = res_json.get('data').get('has_password')
                if not_exsist_message == True:
                    msg = 'User Doesnot Exist on Food Panda   :: '+str(phone)
                    dict = {'message':msg}
                    return dict
                else:
                    res = res_json.get('data').get('items')
                    for value in res:
                        violation = value.get('violation_messages')
                    if violation:
                        msg = 'Access Denied Violation Message'

                        dict = {'message':msg,'Violation_message':violation}
                        return dict

        
    except:
        msg = 'Access Denied Captcha Page '
        dict = {'message':msg}
        return dict

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)