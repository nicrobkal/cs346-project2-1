#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
Topic = form.getvalue('Topic')
Username  = form.getvalue('Username')

print("Content-Type: text/html;charset=utf-8")
print()
print('<html>')
print('<head>')
print('<title>Hello Word - First CGI Program</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! This is my first CGI program</h2>')
print('<h3>Topic: ' + Topic + ' Username: ' + Username + '</h3>')
print('</body>')
print('</html>')
