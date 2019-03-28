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



# this function handles the processing of the actual text of the HTML file.
# It writes everything from the HTML header, to the content in the body, to
# the closing tags at the bottom.
#
# Later, I ought to make this smarter, to handle cookies and such.  Or, just
# switch over to some framework which makes it all easier for me!

def write_html():
    # see https://docs.python.org/3.4/library/cgi.html for the basic usage
    # here.
    form = cgi.FieldStorage()


    gameNum = 1234
    players = ["Russ","Eric"]
    size = 3
    state = "Active"
    nextToPlay = 0
    curUser = 0

    last = "1 Jan 1970"

    if "new_game" in form:
        new_game = int(form["new_game"].value)
    else:
        new_game = None


    print(""" <html>
	<h1>Skype '85</h1>
	<body>
		<fieldset>
			<legend> <font size="+2"> <b>Create New Conversation</b> </font> </legend>
			<p>
				<form action="create_game.py" method="post" id="newConversation">
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
									<input type="text" name="Topic" value="Memes"><br>
								</td>
								<td>
									<input type="text" name="Username" value="GrumpyCat"><br>
								</td>
								<td>
                                                                        <input type="text" name="Text" size="127" value="First Post!"><br>
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

    cursor.close();


    # now, search for the games that *HAVE* been completed.
    cursor = conn.cursor()
    # cursor.execute("SELECT id,player1,player2,size,state FROM games WHERE state IS NOT NULL;")

    cursor.close();
    conn.close();


    idle = ""
    # idle     = [{"key":5678, "player0_name":"Russ", "player1_name":"Eric", "size":3, "last_activity":"A long time ago..."}]

    write_conversation_table(active)

    print("""					<tbody>
					</table>
				</form>
		</fieldset>
	</body>
</html>

""", end="")



def write_table(desc, games, new_game=None, idle=False, finished=False):
    if idle:
        idleStr = "<td><b>Idle Since</b></td> "
    else:
        idleStr = ""

    if finished:
        finishedStr = "<td colspan=2><b>Winner</b></td> "
    else:
        finishedStr = "<td><b>Play as...</b></td>"

    print("""<p>
<font size="+1"><b>%s Games</b></font>
  <br><table border=1>
        <tr> <td><b>ID</b></td> <td><b>Players</b></td> <td><b>Size</b></td> %s%s</tr>
""" % (desc, idleStr,finishedStr), end="")

    for g in games:
        key     =  g["key"]
        players = [g["player0_name"], g["player1_name"]]
        size    =  g["size"]

        if new_game is not None and key == new_game:
            mark1 = "<font color=red><b>"
            mark2 = "</b></font>"
        else:
            mark1 = ""
            mark2 = ""


        if idle:
            idleStr = "          <td>%s</td>\n" % g["last_activity"]

        if not finished:
            finishedStr = """          <td> %s<a href="game.py?user=%s&game=%d">%s</a> <a href="game.py?user=%s&game=%d">%s</a>%s </td>
""" % (mark1, players[0],key,players[0], players[1],key,players[1], mark2)
        else:
            winner = g["winner"]
            finishedStr = "          <td>%s</td> <td>(%s)</td>\n" % (winner[0],winner[1])


        print("""
        <tr>
          <td>%s%d%s</td> <td>%s%s, %s%s</td> <td>%s%dx%d%s</td>
%s%s        </tr>
""" % (mark1,key,mark2, mark1,players[0],players[1],mark2, mark1,size,size,mark2, idleStr,finishedStr), end="")

    print("""      </table>


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


def write_create_game_form():
    print("""<p><b>Create a New Game</b>

<form action="create_game.py" method="post">
  Player 1: <input type="text" size=10 name="player1">
  Player 2: <input type="text" size=10 name="player2">
  Size:     <input type="text" size=1  name="size">
  <input type=submit value="Create">
</form>

""", c[0], c[1], end="")



# this is what actually runs, each time that we are called...

#print("Content-Type: text/plain;")
#print()

print("Content-Type: text/html;charset=utf-8")
print()

write_html()

