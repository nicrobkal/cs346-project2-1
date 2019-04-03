#! /usr/bin/env python3

import cgi
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

def process_form():
    form = cgi.FieldStorage()

    if "Topic" not in form or "Username" not in form or "Text" not in form:
        raise FormError("Invalid parameters.")

    topic = form["Topic"].value
    username = form["Username"].value
    firstPost = form["Text"].value
    for c in topic+username:
        if c not in "_-" and not c.isdigit() and not c.isalpha():
            raise FormError("Invalid parameters: The topic and username can only contains upper and lowercase characters, digits, underscores, and hypens")
            return

    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           port   = 3306,
 			   user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)
    cursor = conn.cursor()

    # Insert new rows
    cursor.execute("""INSERT INTO Conversations(Topic,Username) VALUES('%s','%s');""" % (topic,username))
    cursor.execute("""INSERT INTO Posts(Topic,OriginUsername,Username,Text,Likes) VALUES("%s","%s","%s","%s","%d");""" % (topic,username,username,firstPost,0))

    conn.commit()
    cursor.close()
    conn.close()

    return topic,username



# Main function
try:
    topic,username = process_form()

    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/project2/list.py""" % (pnsdp.WEB_HOST))
    print()

except FormError as e:
    print("""Content-Type: text/html;charset=utf-8

<html>

<head><title> Skype 1985 </title></head>

<body>

<p>ERROR: %s

<p><a href="list.py">Return to conversations list</a>

</body>
</html>

""" % e.msg, end="")

except:
    raise
