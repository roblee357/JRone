from __future__ import print_function
from flask import Flask, request
from flask.ext.cors import CORS
from datetime import datetime
import os, traceback, sys 
import json
import os

app = Flask('__name__')
cors = CORS(app)
data_tail = 20
@app.route('/',methods=['GET','POST','OPTIONS'])                                                                                                                                         
def recive_fe_events():
    try:
        data = request.get_data()
	#dataf = ""
        if request.content_length < 20000 and request.content_length != 0:
           # filename = 'out/{0}.json'.format(str(datetime.now()))
           ## Delete lines before last data_tail
           i=0
           with open('detectLog.txt', 'r') as f:
                for line in f:
                    i = i + 1
                if i > data_tail+1:
                    with open('detectLog.txt', 'r') as f:
                        for x2 in range(i - data_tail-1):
                            f.readline()
                        for line in f:
                            content = f.readlines()
                    with open('detectLog.txt', 'w') as f:
                          f.writelines(content)
                    with open('detectLog.txt', 'a+') as f:
                          f.write(str(data.decode())+'\n')
                else:
                    with open('detectLog.txt', 'a+') as f:
                        f.write(str(data.decode())+'\n')
        else:
            print("Request too long", request.content_length)
            content = '{{"status": 413, "content_length": {0}, "content": "{1}"}}'.format(request.content_length, data)
            return content, 413 
    except:
        traceback.print_exc()
        return None, "Everything is OK" # status.HTTP_500_INTERNAL_SERVER_ERROR

    return '{"status": 200}\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int("5002"))
