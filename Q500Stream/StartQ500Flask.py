from __future__ import print_function
from flask import Flask, request
from flask.ext.cors import CORS
from datetime import datetime
import os, traceback, sys 
import json
import os

app = Flask('__name__')
cors = CORS(app)

@app.route('/',methods=['GET','POST','OPTIONS'])                                                                                                                                         
def recive_fe_events():
    try:
        data = request.get_data()
	#dataf = ""
        if request.content_length < 20000 and request.content_length != 0:
           # filename = 'out/{0}.json'.format(str(datetime.now()))
            with open('Q500log.txt', 'a+') as f:
                 f.write(str(data)+'\n')
        else:
            print("Request too long", request.content_length)
            content = '{{"status": 413, "content_length": {0}, "content": "{1}"}}'.format(request.content_length, data)
            return content, 413 
    except:
        traceback.print_exc()
        return None, "Everything is OK" # status.HTTP_500_INTERNAL_SERVER_ERROR

    return '{"status": 200}\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int("5004"))
