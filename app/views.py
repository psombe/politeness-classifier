from app import app
from flask import request
import json
import cPickle as pickle

from politeness import model

print 'loaded classifier'
                                                                                  
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/politeness',methods=['GET', 'POST'])
def politeness():
    '''Method to get politeness score'''
    try:
        if request.method == 'POST':
            try:
                sentence = request.form[u'sentence']
                try:
                    result = model.get_score(sentence)
                except Exception as e:
                    raise ValueError(e.message)
                if(request.form.has_key('pthr')): pthr = float(request.form[u'pthr'])
                else: pthr = 0.15
                if(request.form.has_key('ipthr')): ipthr = float(request.form[u'ipthr'])
                else: ipthr = 0.15
                ipthreshold = ipthr
                pthreshold = pthr
                print result
                ans = 'Impolite' if (result['impolite'] >= (.5 + ipthreshold)) else ('Neutral' if (result['impolite'] >= (0.5 - pthreshold)) else 'Polite')
                res = {}
                res['score'] = ans
                res['value'] = result
                res['msg'] = "Fine"
                return json.dumps(res)
            except KeyError:
                raise ValueError("Using POST. No sentence detected.")
        else:
                return "Using GET. Use POST instead. "
    except ValueError as e:
        errres = {}
        errres['score'] = 'Neutral'
        errres['value'] = {}
        errres['msg'] = e.message
        return json.dumps(errres)
