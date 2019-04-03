#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

form = cgi.FieldStorage()

if "Username" not in form or "Text" not in form or "Topic" not in form or "OriginUsername" not in form:
    raise FormError("Invalid parameters: Username//Text//Topic//Original Username not in form")

topic = form.getvalue('Topic')
username = form.getvalue('Username')
originUsername = form.getvalue('OriginUsername')
text = form.getvalue('Text')

for c in topic+username:
    if c not in "_-" and not c.isdigit() and not c.isalpha():
        raise FormError("Invalid parameters: The topic and username can only contains upper and lowercase characters, digits, underscores, and hypens")

#connect to the database
conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
    port   = 3306,
    user   = pnsdp.SQL_USER,
    passwd = pnsdp.SQL_PASSWD,
    db     = pnsdp.SQL_DB)

cursor = conn.cursor()

cursor.execute("""INSERT INTO Posts(Topic,OriginUsername,Username,Text,Likes) VALUES("%s","%s","%s","%s","%d");""" % (topic,originUsername,username,text,0))

conn.commit()
cursor.close()
conn.close()

try:
    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/project2/conversation.py?Topic=%s&Username=%s""" % (pnsdp.WEB_HOST, topic, originUsername))
    print()

except FormError as e:
    print("""Content-Type: text/html;charset=utf-8
<html>
<head><title>ERROR FORM</title></head>
<body>
<p>ERROR: %s
<p><a href="list.py">Return to conversation list</a>
</body>
</html>
""" % e.msg, end="")

except:
    print("""Content-Type: text/html;charset=utf-8\n\n""")

    raise
