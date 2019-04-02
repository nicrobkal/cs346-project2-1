#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")


import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

form = cgi.FieldStorage()

if "OriginUsername" not in form or "PostNum" not in form or "Topic" not in form:
    raise FormError("Invalid parameters: Username//Text//Topic//Original Username not in form")

postNum = form.getvalue('PostNum')
topic = form.getvalue('Topic')
originUsername = form.getvalue('OriginUsername')

#connect to the database
conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
    port   = 3306,
    user   = pnsdp.SQL_USER,
    passwd = pnsdp.SQL_PASSWD,
    db     = pnsdp.SQL_DB)

cursor = conn.cursor()

cursor.execute("""UPDATE Posts SET Likes=Likes-1 WHERE (PostNum='%s' AND Topic='%s');""" % (postNum, topic))

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
<head><title>Skype 1985</title></head>
<body>
<p>ERROR: %s
<p><a href="list.py">Return to game list</a>
</body>
</html>
""" % e.msg, end="")

except:
    print("""Content-Type: text/html;charset=utf-8\n\n""")

    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error
