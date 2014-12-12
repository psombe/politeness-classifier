#!/usr/bin/env python

import sys
sys.path.append('..')

import time

import pusherclient
import pusher
import json
import logging

from politeness import model

global pushercl

# Add a logging handler so we can see the raw communication data
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

def print_usage(filename):
    print("Usage: python %s <appkey>" % filename)

def politeness(request):
	'''Method to get politeness score'''
	try:
		print "Reached", type(request)
		print "request is", request
		sentence = request[u'sentence']
		print "sentence is", sentence 
		try:
    			result = model.get_score(sentence)
		except Exception as e:
			raise ValueError(e.message)
		if(request.has_key('pthr')): pthr = float(request[u'pthr'])
		else: pthr = 0.15
		if(request.has_key('ipthr')): ipthr = float(request[u'ipthr'])
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
		raise ValueError("No sentence detected")
	except ValueError as e:
    		errres = {}
    		errres['score'] = 'Neutral'
    		errres['value'] = {}
    		errres['msg'] = e.message
    		return json.dumps(errres)

p = pusher.Pusher(
  app_id='97110',
  key='39e6e5877f5938c63b3b',
  secret='3d737a31fad3fa30d6b0'
)

def channel_callback(data):
    print("Channel Callback: %s" % data)
    resp = politeness(json.loads(data))
    print resp
    p['push_channel'].trigger('push_event', {'message': json.dumps(resp)})
    p['test_channel'].trigger('my_event', {'message': json.dumps(resp)})


def connect_handler(data):
    channel = pushercl.subscribe("sub_channel")
    channel.bind('sub_event', channel_callback)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage(sys.argv[0])
        sys.exit(1)

    appkey = sys.argv[1]

    pushercl = pusherclient.Pusher(appkey)

    pushercl.connection.bind('pusher:connection_established', connect_handler)
    pushercl.connect()

    while True:
        time.sleep(1)
