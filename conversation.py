#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import MySQLdb

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


#def create_table():
#    conn = MySQLdb.connect(host = "cs346-project2-1.cbhi0v14khzk.us-west-2.rds.amazonaws.com",
#        user = "nicrobkal",
#        port = 3306,
#        passwd = "Cosmo123$%",
#        db = "cs346_project2")
#
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM Conversations;") #WHERE Topic='%s' AND Username='%s'
#
#    active = []
#    for row in cursor.fetchall():
#        active.append([row[0], row[1], row[2], row[3], row[4]])
#
#    cursor.close()
#    conn.close()
#
#    print("<!-- %s -->", '\n'.join([' '.joint(word for word in line]) for line in row]))
#
#    for c in active:
#        print("""
#                        <tr>
#                            <td>
#                                <p>%s<br><h3>%s &#09 %s &#09 %d</h3></p>
#                            </td>
#                        </tr>
#                        
#        """ % (active[2], active[1], active[3], active[4]), end="")


print("""Content-Type: text/html;charset=utf-8

<html>
    <head>
        <title>Skype 1985</title>
    </head>
    <body>
        <header><h1>Conversation Name: %s</h1></header>
        <fieldset>
            <legend> <font size="+2"> <b>New Post</b> </font> </legend>
            <p>
                <form action="conversation.py" method="post" id="addText">
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    New Text:
                                </td>
                                <td>
                                    Username:
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <input type="text" name="Topic" size="127" value=""><br>
                                </td>
                                <td>
                                    <input type="text" name="Username" value=""><br>
                                </td>
                                <td>
                                    <button type="submit" form="addText" value="Submit">Submit</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </form>
            </p>
        </fieldset>
        <fieldset>
            <legend> <font size="+2"> <b>Posts</b> </font> </legend>
            <form action="conversation.py" method="post" id="updateUpvoteCount">
                <table>
                    <tbody>
                    <!--- Text insertion starts here -->""" % (Topic))

#create_table()

print("""
                    <!--- Text insertion ends here -->
                    </tbody>
                </table>
            </form>
        </fieldset>
         
        <h3>Topic: %s Username: %s </h3>
    </body>
</html>""" % (Topic, Username))
