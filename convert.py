import http.client
import json
import logging

class NoRateDefinedExeption(Exception):
    def __init__(self,currency):
        super().__init__("No exchange value for <<"+currency+">> found.")


class Exchange:

    def load_currencies(self):
        connect = http.client.HTTPSConnection("api.exchangeratesapi.io")
        connect.request("GET","/latest")
        str = connect.getresponse().read().decode()
        connect.close()
        j=json.loads(str)
        
        self.currencies={}
        for cur in j['rates']:
            self.currencies[cur.upper()]=float(j['rates'][cur])
        
        self.currencies['EUR']=1

    def get_exchange_rate(self,curr):
        curr = curr.upper()
        try:
            return self.currencies[curr]
        except Exception as ex:
            raise NoRateDefinedExeption(curr)

    def convert(self,value,c1,c2):
        r1 = self.get_exchange_rate(c1)
        euro = value/r1
        r2 = self.get_exchange_rate(c2)

        return euro*r2        


def test_exchange_API():
    ex = Exchange()
    ex.load_currencies()
    test_curs= ['RUB','EUR','USD']
    for cur in test_curs:
        logging.info("Currency echange rate to EUR %s-%f"%(cur,ex.get_exchange_rate(cur)))

    try:
        logging.info(ex.get_exchange_rate('XXX'))
        raise Exception("No value for currency XXX should be found!")
    except Exception as e:
        logging.info(e)

    test_pairs = [("USD","RUB"),("RUB","usd"),("USD","eur"),("EUR","USD"),("eur","EUR"),("USD","USD")]

    for (cur1,cur2) in test_pairs:
        logging.info("Convert 1 %s to %s - %f"%(cur1,cur2,ex.convert(1,cur1,cur2)))

if __name__ == "__main__":        
    test_exchange_API()

