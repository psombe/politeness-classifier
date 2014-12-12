#Politeness Classifier

##Dependencies:
This classifier requires 2 other packages:
1. [Stanford Politeness API] (https://github.com/sudhof/politeness)
2. [Stanford Core NLP python flavour] (https://bitbucket.org/torotoki/corenlp-python)

##Python Packages
1. nltk
2. scipy
3. scikit\_learn
4. numpy
5. flask
6. json
7. cPickle
8. requests
9. OpenSSL (optional)

##Setup Instructions:
1. Core NLP server
  1. Follow the instructions mentioned in the package
  2. The politeness classifier works with [Version 1.3.3] (http://nlp.stanford.edu/software/stanford-corenlp-2012-07-09.tgz)
  3. Run the server on port 8080 (the default port)
  4. Sample startup command(s)
    1. `python corenlp/corenlp.py -S stanford-corenlp-2012-07-09/
    2. Ideally the server should be started as a background process and logging can be added with the following command
    3. `setsid python corenlp/corenlp.py -S stanford-corenlp-2012-07-09/ < /dev/zero 2>&1&> ~/logs/coreNLP-`date '+%Y.%m.%d'`.log &
  5. The Core NLP package require at least 3GB of RAM to run.
2. Classifier Server
  1. Follow the basic instructions described in this [great blog post] (http://blog.garethdwyer.co.za/2013/07/getting-simple-flask-app-running-on.html) 
  2. Requires an Apache webserver and Python WSGI module
  3. Some minor modifications from the tutorial for setting up the webpage for the server: 
    1. Instead of "sudo nano sitename.com" do "sudo nano sitename.conf" 
    2. Instead of "sudo a2dissite default" do "sudo a2dissite 000-default.conf"
    3. Instead of "sudo a2ensite sitename.com" do "sudo a2ensite sitename.conf"
    4. a2dissite disables the site and a2ensite enables it
    5. Here we have created the config files for the webpage
  4. In the run.py add host='0.0.0.0' inside of run()
  5. Start the server
    1. `sudo python run.py
    2. Ideally the server should be started as a background process with logging like so
    3. `setsid python run.py < /dev/zero 2>&1&> ~/logs/politeness-`date '+%Y.%m.%d'`.log &
    4. By default the classifier/flask is running on port 5000
  6. Setting up HTTPS/SSL connection (optional)
    1. An HTTPS server can be setup with the following additions
    2. Obtain a valid SSL certificate and key. Store them as server.crt and server.key respectively.
    3. We need to make some minor changes to the config files created in step 3.
      1. In the sitename.conf add the SSL config parameters in the Virtual Host tab. The final conf should look like this.
         ```
	 <VirtualHost *:80>
     	 WSGIScriptAlias / /var/www/politeness/flask_politeness/flask_politeness.wsgi
     	 *SSLEngine on*
     	 *SSLCertificateFile /home/srinivas/Keys/server.crt*
     	 *SSLCertificateKeyFile /home/srinivas/Keys/server.key*  

     	 <Directory /var/www/politeness/flask_politeness>
            WSGIProcessGroup flask_politeness
         WSGIApplicationGroup %{GLOBAL}
         Order deny,allow
         Allow from all
     	 </Directory>
         ```
      2. Restart the Apache server to pick up the new config
      3. `sudo /etc/init.d/apache2 restart
    4. Modify run.py to pick up the SSL context (this should be just uncommenting the first few lines and commenting out the current app.run() )

##Making a Request
There are two ways to test the classifier
1. Programmatically
  1. Use the trial.py script and modify the url to point to the classifier.
2. If the classifier is running on an EC2 instance
  1. Go to a browser, check for the EC2 public IP in the URL bar. Something other than a 404 page should appear.
  2. Go to the RESTClient installed on Firefox.
  3. Use the following config:
    1. Method => POST
    2. URL => http://yourIP:5000/politeness
    3. Header => Content-Type = application/x-www-form-urlencoded
    4. Body => sentence=\"your sentence goes here\"
    5. The politeness scores should appear.
