from convert import Exchange

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs


import logging
logging.getLogger().setLevel(logging.INFO)

exchange = Exchange()
hostName =  "0.0.0.0"
serverPort = 8080
explanation = "Sample URL: %s:%d/exchange?USD=11" % (hostName,serverPort)

class MyServer(BaseHTTPRequestHandler):
    error_content_type="application/json"
    error_message_format = """\
{
    "error": {
        "message": "%(message)s",
        "code": %(code)s,
        "explain": "%(explain)s"
    }
}
"""

    def do_GET(self):
        u = urlparse(self.path)
        p = u.path
        q = parse_qs(u.query)
    
        value = 0
        if not p=="/exchange":
            self.send_error(404,explanation)
            return

        if 'USD' in q.keys():
            try:
                value = float(q['USD'][0])
            except Exception:
                self.send_error(400,"Wrong amount('%s') provided. " % q['USD'][0]+explanation)
                return
        else:
            self.send_error(400,"No valid currency ('USD') given. "+explanation)
            return

        if value<0:
            self.send_error(400,"Negative values (%d) not allowed."%value)
            return

        convert=0
        try:
            convert = exchange.convert(value,"usd","rub")
        except Exception as ex:
            self.send_error(500,"Exchange unavailable."+str(ex))
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()


        self.wfile.write(bytes("{\"RUB\" : %f " % convert, "utf-8"))
        self.wfile.write(bytes(", \"USD\" : %f}\n" % value, "utf-8"))
        

def serverstart():      
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    logging.info("Server started http://%s:%s" % (hostName, serverPort))

    try:
        logging.info("Connecting to currency exchange...")
        exchange.load_currencies()
    except Exception as e:
        logging.error("Exchange unavailable: %s"%str(e))
        exit()


    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()

if __name__ == "__main__":  
    serverstart()
