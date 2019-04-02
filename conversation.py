#! /usr/bin/env python3

import MySQLdb

import cgi
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

form = cgi.FieldStorage() 

Topic = form.getvalue('Topic')
Username  = form.getvalue('Username')

print("""Content-Type: text/html;charset=utf-8

<html>
    <head>
        <title>Skype 1985</title>
    </head>
    <body>
        <header><h1>%s</h1>
        <h3><a href="list.py">Return to conversations list</a><h3>
        </header>
        <fieldset>
            <legend> <font size="+2"> <b>New Post</b> </font> </legend>
            <p>
                <form action="create_post.py" method="post" id="addText">
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    New Post:
                                </td>
                                <td>
                                    Username:
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <input type="text" name="Text" size="127" value=""><br>
                                </td>
                                <td>
                                    <input type="text" name="Username" value=""><br>
                                </td>
                                <td>
				    <input type="hidden" name="Topic" value="%s" />
				    <input type="hidden" name="OriginUsername" value="%s" />
				</td>
				<td>
                                    <button type="submit" value="Submit">Submit</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
           	</form>
            </p>
        </fieldset>
        <fieldset>
            <legend> <font size="+2"> <b>Posts</b> </font> </legend>
                <!--- Text insertion starts here -->""" % (Topic, Topic, Username))

conn = MySQLdb.connect(host = "cs346-project2-1.cbhi0v14khzk.us-west-2.rds.amazonaws.com",
    user = "nicrobkal",
    port = 3306,
    passwd = "Cosmo123$%",
    db = "cs346_project2")

cursor = conn.cursor()
cursor.execute("""SELECT * FROM Posts WHERE Topic='%s' AND OriginUsername='%s';""" %(Topic, Username))

active = []
for row in cursor.fetchall():
    active.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

cursor.close()
conn.close()

for c in active:
	
    print(""" 
                                                       	<fieldset> <legend> <b>%s</b></legend> 
                                                       	<table>
							<tbody>
								<tr>
									%s
									<td>
										&nbsp %s &nbsp
									</td>
									<td>
										%s &nbsp
									</td>
									<td>
										<form action="upvote.py" method="post" id="upvote">
                                                        			<input type="hidden" name="Topic" value="%s" />
                                                        			<input type="hidden" name="OriginUsername" value="%s" />
                                                        			<input type="hidden" name="PostNum" value="%s" />
										&nbsp<button type="submit" value="Submit">👍 Upvote</button>&nbsp
										</form>
 									</td>
									<td>
										<form action="downvote.py" method="post" id="downvote">
                                                        			<input type="hidden" name="Topic" value="%s" />
                                                        			<input type="hidden" name="OriginUsername" value="%s" />
                                                        			<input type="hidden" name="PostNum" value="%s" />
										&nbsp<button type="submit" value="Submit">👎 Downvote</button>&nbsp
										</form>
									</td>
								</tr>
							</tbody>
						</table>
						</form>
					</fieldset>
 
   """ % (c[3], c[4], c[5], c[6], c[1], c[2], c[0], c[1], c[2], c[0]))

print("""
                    <!--- Text insertion ends here -->
            </form>
        </fieldset>
    </body>
</html>""")
