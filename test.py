import inspect
import http.client
import logging
logging.getLogger().setLevel(logging.INFO)

import client,server,convert
modules = [client,server,convert]

import subprocess,time

if __name__ == "__main__":        

    conn = http.client.HTTPConnection(server.hostName,server.serverPort)
    proc=None
    try:
        conn.connect()
    except:
        logging.info("Starting server process...")
        proc = subprocess.Popen("exec python3 server.py",shell=True)
        time.sleep(4)
    finally:
        conn.close()

    tests = {}
    failed=False

    for m in modules:
        funs = inspect.getmembers(m, inspect.isfunction)
    
        for (name,f) in funs:
            if name.startswith('test'):
                logging.info ("Running test function %s :"%name)

                try:
                    f()
                    tests[name]=True
                except Exception as ex:
                    logging.error("Did not pass."+str(ex))
                    tests[name]=False


    logging.info("\nTesting summary:")
    for name in tests:
        if tests[name]:
            logging.info("%s passed."%name)
        else:
            failed=True
            logging.info("%s failed."%name)

    if failed:
        logging.error("Some tests failed. Pay attention to the logs")
    else:
        logging.info("Tests passed. Ok")

    if proc:
        logging.info("Killing server process...")
        proc.terminate()