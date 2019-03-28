#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")


import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError



# this function handles the processing of the actual text of the HTML file.
# It writes everything from the HTML header, to the content in the body, to
# the closing tags at the bottom.
#
# Later, I ought to make this smarter, to handle cookies and such.  Or, just
# switch over to some framework which makes it all easier for me!

def process_form():
    # see https://docs.python.org/3.4/library/cgi.html for the basic usage
    # here.
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

    # insert the new row
    cursor.execute("""INSERT INTO Conversations(Topic,Username,Text,Time,Likes) VALUES('%s','%s','%s','%s','%d');""" % (topic,username,firstPost,"2018-01-12",0))


    # MySQLdb has been building a transaction as we run.  Commit them now, and
    # also clean up the other resources we've allocated.
    conn.commit()
    cursor.close()
    conn.close()

    return topic,username



# this is what actually runs, each time that we are called...

try:
    #print("Content-type: text/html")
    #print()

    # this will not print out *ANYTHING* !!!
    topic,username = process_form()

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/project2/list.py""" % (pnsdp.WEB_HOST))
    print()

except FormError as e:
    print("""Content-Type: text/html;charset=utf-8

<html>

<head><title> Skype 1985 </title></head>

<body>

<p>ERROR: %s

<p><a href="list.py">Return to game list</a>

</body>
</html>

""" % e.msg, end="")

except:
    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error


