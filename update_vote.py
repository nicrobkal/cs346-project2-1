#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

def process_form():
    form = cgi.FieldStorage()

    post_id = form["post_id"].value
    mod_amt = form["mod_amt"].value
    topic = form["Topic"].value
    username = form["Username"].value

    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           port   = 3306,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)
    cursor = conn.cursor()

    cur_votes = cursor.execute("""SELECT Likes FROM Posts WHERE PostNum='%s');""" % (post_id))
    cursor.execute("""UPDATE Posts SET Likes = %d WHERE PostNum='%s');""" % ((cur_votes += mod_amt), post_id))
    
    cursor.close()
    conn.close()

    return topic, username

try:
    topic, username = process_form()

    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/project2/conversation.py?Topic=%s&Username=%s""" % (pnsdp.WEB_HOST, topic, username))
    print()
