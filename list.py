#! /usr/bin/env python3

import cgi
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp



# This function writes the main html that surrounds the unique html generated
# using a database.

def write_html():
    form = cgi.FieldStorage()

    print(""" <html>
	<h1>Skype '85</h1>
	<body>
		<fieldset>
			<legend> <font size="+2"> <b>Create New Conversation</b> </font> </legend>
			<p>
				<form action="create_conversation.py" method="post" id="newConversation">
					<table>
						<tbody>
							<tr>
								<td>
									Topic:
								</td>
								<td>
									Username:
								</td>
								<td>
                                                                        First Post:
                                                                </td>
							</tr>
							<tr>
								<td>
									<input type="text" name="Topic" value=""><br>
								</td>
								<td>
									<input type="text" name="Username" value=""><br>
								</td>
								<td>
                                                                        <input type="text" name="Text" size="127" value=""><br>
                                                                </td>
								<td>
									<button type="submit" form="newConversation" value="Submit">Submit</button>
								</td>
							</tr>
						<tbody>
					</table>
				</form>
			</p>
		</fieldset> 
                <fieldset>
                <legend> <font size="+2"> <b>Previous Conversations</b> </font> </legend>
""", end="")

    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
			   port   = 3306,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)


    # search for all conversations that have been started
    cursor = conn.cursor()
    cursor.execute("SELECT Topic,Username FROM Conversations;")

    active = []
    for row in cursor.fetchall():
        active.append([row[0], row[1]])

    if active:
        print("""
                                <form action="join_game.html" method="post" id="joinConversation">
                                        <table>
                                                <table border="1">
                                                <tbody>
                                                        <tr>
                                                                <td>
                                                                        Topic
                                                                </td>
                                                                <td>
                                                                        Created By
                                                                </td>
                                                        </tr>


        """, end="")
    else:
        print("No Conversations Yet!")

    cursor.close();


    write_conversation_table(active)

    print("""					<tbody>
					</table>
				</form>
		</fieldset>
	</body>
</html>

""", end="")


def write_conversation_table(conversations):

	for c in conversations:
		print("""
							<tr>
								<td>
									%s
								</td>
								<td>
									%s
								</td>
								<td>
									<a href="conversation.py?Topic=%s&Username=%s">Join Conversation</a>
								</td>
							</tr>

		""" % (c[0], c[1], c[0], c[1]), end="")


# Main function

print("Content-Type: text/html;charset=utf-8")
print()

write_html()
