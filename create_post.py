#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")


import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

form = cgi.FieldStorage()

username = form.getvalue('Username')

print()

if "Username" not in form or "Text" not in form or "Topic" not in form:
    raise FormError("Invalid parameters.")

topic = form["Topic"].value
username = form["Username"].value
originUsername = form["OriginUsername"].value
firstPost = form["Text"].value
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

cursor.execute("""INSERT INTO Posts(Topic,OriginUsername,Username,Text,Time,Likes) VALUES('%s','%s','%s','%s','%s','%d');""" % (topic,originUsername,username,firstPost,"2018-01-12",0))

conn.commit()
cursor.close()
conn.close()

print("Status: 303 See other")
print("""Location: http://%s/cgi-bin/project2/conversation.py""" % (pnsdp.WEB_HOST))
print()
