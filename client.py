import json
import http.client
import server

import logging

logging.getLogger().setLevel(logging.INFO)

def request(value,server=server.hostName,port=server.serverPort):
    try:
        conn = http.client.HTTPConnection(server,port)
        conn.request("GET","/exchange?USD="+str(value))
        resp = conn.getresponse().read().decode()
        conn.close()
    except Exception as ex:
        raise ex
    
    j = json.loads(resp)
    if 'error' in j:
        raise Exception(str(j))
    return j

def convert(value):
    return request(value)['RUB']


def test_client():

    logging.info("Converting 11 USD to rub - %f "%convert(11))

    try:
        logging.info(convert('11f'))
        raise Exception("Should be error if '11f' USD given")
    except Exception as ex:
        logging.info("Good. Error cought :"+str(ex))

    try:
        logging.info(convert('-11'))
        raise Exception("Should be error if '-11'(negative value) USD given")
    except Exception as ex:
        logging.info("Good. Error cought :"+str(ex))


if __name__ == "__main__":        
    test_client()