#!/usr/bin/python2.7
#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')

from app import app
#app.run(debug = True,ssl_context = context)
app.run(debug = True)
