#!/usr/bin/python

# Required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

import cgi, MySQLdb
import cgitb; cgitb.enable() 

#load up the form
form=cgi.FieldStorage()

#create a db connection
try:
	conn = MySQLdb.connect (host = "bankc35320110808.db.7939020.hostedresource.com",
						   user = "bankc35320110808",
						   passwd = "comP353",
						   db = "bankc35320110808")
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)
	
cursor = conn.cursor ()

if form.has_key("action") and form["action"].value!="":
	if form["action"].value=="c":
		#client choices
		cursor.execute ("""
			SELECT client.client_id, client.name
			FROM client
		""")
		rows = cursor.fetchall ()
		clients=""
		for row in rows:
			clients+='<option value="%s">Client ID: %s, Client: %s</option>' % (row[0], row[0],row[1])
		
		#option choices
		cursor.execute ("""
			SELECT option_id, plan.option, transaction_limit, credit_limit, charge
			FROM plan
		""")
		rows = cursor.fetchall ()
		options=""
		for row in rows:
			options+='<option value="%s">Option: %s, T_limit: %s, C_limit: %s, Charge: %s</option>' % (row[0],row[1],row[2],row[3],row[4])
			
		#type choices
		cursor.execute ("""
			SELECT type_id, type, percentage
			FROM rate
		""")
		rows = cursor.fetchall ()
		rates=""
		for row in rows:
			rates+='<option value="%s">Type: %s, Percentage: %s</option>' % (row[0], row[1],row[1])
			
			
		html= """
			Create Account
			<form id="accountCreate" action="account.cgi" method="post">	
				<input type="hidden" name="accountCreate" value="1"/>
				Balance: <input type="text" name="balance" value="0"/> <br />
				<select name="clients" />
					%s
				</select> <br />
				<select name="options" />
					%s
				</select> <br />
				<select name="rates" />
					%s
				</select> <br />
				<input type="submit" value="go" />
			</form>
		""" % (clients, options, rates)
	elif form["action"].value=="r":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s</option>' % (row[0],row[0], row[2])
		
		html= """
			Select Account to Read
			<form id="accountRead" action="account.cgi" method="post">	
				<select name="accountRead" />
					%s
				</select>

				<input type="submit" value="go" />
			</form>
		""" % str
	elif form["action"].value=="u":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s</option>' % (row[0],row[0], row[2])
		
		html= """
			Select Account to Update
			<form id="accountUpdate" action="account.cgi" method="post">	
				<select name="accountUpdate" />
					%s
				</select>

				<input type="submit" value="go" />
			</form>
		""" % str
	elif form["action"].value=="d":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s</option>' % (row[0],row[0], row[2])
		
		html= """
			Select Account to Delete
			<form id="accountDelete" action="account.cgi" method="post">	
				<select name="accountDelete" />
					%s
				</select>

				<input type="button" onclick="if (confirm('sure?')) submit();" value="delete">
			</form>
		""" % str
	else:
		html="none"


elif form.has_key("accountRead") and form["accountRead"].value!="":
	query="""
			SELECT account_number, balance, 
					plan.option, plan.transaction_limit, plan.credit_limit, plan.charge,
					rate.type, rate.percentage,
					client.name
			FROM account, client, plan, rate
			WHERE account_number=%s AND 
					account.client_id=client.client_id AND 
					plan.option_id=account.option AND 
					rate.type_id=account.type
		""" % form["accountRead"].value
	cursor.execute (query) 
	row = cursor.fetchone ()
	
	html= """
			<ul>
				<li>Account Number: %s</li>
				<li><b>Balance</b>: %s</li>
				<li>Option: %s</li>
				<li>Option Transaction Limit: %s</li>
				<li>Option Credit Limit: %s</li>
				<li>Option Charge: %s</li>
				<li>Rate: %s</li>
				<li>Rate Percentage: %s</li>
				<li><b>Client</b>: %s</li>
			</ul>

	""" %(row[0],row[1],row[2], row[3], row[4], row[5], row[6], row[7], row[8])

elif form.has_key("accountCreate") and form["accountCreate"].value!="":
	try:
		balance=float(form["balance"].value)
	except:
		html="Error with the balance"
	else:
		query="""
			INSERT INTO account(account_number,balance,account.option,type,client_id)
			VALUES(NULL,'%s','%s','%s','%s')
		""" % (balance, form["options"].value, form["rates"].value, form["clients"].value)
		
		if(cursor.execute (query)==1):
			conn.commit()
			html="Account creation successful"
		else:
			html="Something went wrong"
		
elif form.has_key("accountUpdate") and form["accountUpdate"].value!="":
	query="""
			SELECT account_number, balance, 
					plan.option, plan.transaction_limit, plan.credit_limit, plan.charge,
					rate.type, rate.percentage,
					client.name, client.client_id
			FROM account, client, plan, rate
			WHERE account_number=%s AND 
					account.client_id=client.client_id AND 
					plan.option_id=account.option AND 
					rate.type_id=account.type
		""" % form["accountUpdate"].value
	cursor.execute (query) 
	account = cursor.fetchone ()
	
	#client choices
	cursor.execute ("""
		SELECT client.client_id, client.name
		FROM client
	""")
	rows = cursor.fetchall ()
	clients=""
	for row in rows:
		if (row[0]==account[9]):
			clients+='<option selected="yes" value="%s">Client ID: %s, Client: %s</option>' % (row[0], row[0],row[1])
		else:
			clients+='<option value="%s">Client ID: %s, Client: %s</option>' % (row[0], row[0],row[1])
	
	#option choices
	cursor.execute ("""
		SELECT option_id, plan.option, transaction_limit, credit_limit, charge
		FROM plan
	""")
	rows = cursor.fetchall ()
	options=""
	for row in rows:
		if (row[1]==account[2]):
			options+='<option selected="yes" value="%s">Option: %s, T_limit: %s, C_limit: %s, Charge: %s</option>' % (row[0],row[1],row[2],row[3],row[4])
		else:
			options+='<option value="%s">Option: %s, T_limit: %s, C_limit: %s, Charge: %s</option>' % (row[0],row[1],row[2],row[3],row[4])
		
	#type choices
	cursor.execute ("""
		SELECT type_id, type, percentage
		FROM rate
	""")
	rows = cursor.fetchall ()
	rates=""
	for row in rows:
		if (row[1]==account[6]):
			rates+='<option selected="yes" value="%s">Type: %s, Percentage: %s</option>' % (row[0], row[1],row[1])
		else:
			rates+='<option value="%s">Type: %s, Percentage: %s</option>' % (row[0], row[1],row[1])
	
	html= """
		Update Account
		<form id="accountUpdate2" action="account.cgi" method="post">	
			<input type="hidden" name="accountUpdate2" value="1"/>
			<input type="hidden" name="account_number" value="%s" />
			
			Balance: <input type="text" name="balance" value="%s"/> <br />
			<select name="clients" />
				%s
			</select> <br />
			<select name="options" />
				%s
			</select> <br />
			<select name="rates" />
				%s
			</select> <br />
			<input type="submit" value="go" />
		</form>
	""" % (account[0],account[1],clients, options, rates)
	
elif form.has_key("accountDelete") and form["accountDelete"].value!="":
	query="""
		DELETE FROM account
		WHERE account_number=%s
	""" % (form["accountDelete"].value)
	
	if(cursor.execute (query)==1):
		conn.commit()
		html="Account deletion successful"
	else:
		html="Something went wrong"
		

	

print '<html><body><a href="/comp353/beta/">Home</a><br />'
print html
print "</html></body>"

#cursor.execute ("show tables;")
#rows = cursor.fetchall ()

#for row in rows:
#	print row

cursor.close ()
conn.close ()

