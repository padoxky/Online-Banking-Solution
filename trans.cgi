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

def deposit(account,amount):
	try:
		if (amount<0):
			return -2
		
		query="""
			SELECT balance
			FROM account
			WHERE account_number="%s"
		""" % account
		cursor.execute(query)
		balance=cursor.fetchone()
				
		newBalance=float(balance[0])+amount
		
		query1="""
			UPDATE account
			SET balance=%s
			WHERE account_number="%s"
		""" % (newBalance, account)
		query2="""
			INSERT INTO transaction(transaction_id, date, amount, type, account_number)
			VALUE (NULL, NULL, '%s', 'credit', '%s')
		""" % (amount, account)
		
		if(cursor.execute(query1)==1):
			conn.commit()
			#log in transaction table
			cursor.execute(query2)
			conn.commit()
			return newBalance
		else:
			return -1
	except:
		return -1
		
def withdraw(account,amount):
	try:
		if (amount<0):
			return -2
			
		query="""
			SELECT balance
			FROM account
			WHERE account_number="%s"
		""" % account
		cursor.execute(query)
		balance=cursor.fetchone()
		
		newBalance=float(balance[0])-amount
				
		if (newBalance<0):
			return -3
		
		query1="""
			UPDATE account
			SET balance=%s
			WHERE account_number="%s"
		""" % (newBalance, account)
		query2="""
			INSERT INTO transaction(transaction_id, date, amount, type, account_number)
			VALUE (NULL, NULL, '%s', 'debit', '%s')
		""" % (amount, account)
		
		if(cursor.execute(query1)==1):
			conn.commit()
			#log in transaction table
			cursor.execute(query2)
			conn.commit()
			return newBalance
		else:
			return -1
	except:
		return -1
	

if form.has_key("action") and form["action"].value!="":
	if form["action"].value=="d":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name, balance
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
		
		html= """
			Select Account & Specify Amount to Deposit
			<form id="accountDeposit" action="trans.cgi" method="post">	
				<select name="accountDeposit" />
					%s
				</select>
				Amount:<input type="text" name="amount" value="0" />
				<input type="submit" value="go" />
			</form>
		""" % str
	elif form["action"].value=="w":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name, balance
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
		
		html= """
			Select Account & Specify Amount to Withdraw
			<form id="accountWithdraw" action="trans.cgi" method="post">	
				<select name="accountWithdraw" />
					%s
				</select>
				Amount:<input type="text" name="amount" value="0" />
				<input type="submit" value="go" />
			</form>
		""" % str
	elif form["action"].value=="t":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name, balance
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
		
		html= """
			<form id="accountTransfer" action="trans.cgi" method="post">	
				Transfer Amount:<input type="text" name="amount" value="0" /> <br />
				From:
				<select name="accountTransfer1" />
					%s
				</select>
				To:
				<select name="accountTransfer2" />
					%s
				</select>		
				<input type="submit" value="go" />
			</form>
		""" % (str,str)
	elif form["action"].value=="q":
		cursor.execute ("""
				SELECT account_number, account.client_id, client.name, balance
				FROM account, client
				WHERE account.client_id=client.client_id
				ORDER BY account_number
			""")
		rows = cursor.fetchall ()
		
		#build options
		str=""
		for row in rows:
			str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
		
		html= """
			Query Transactions of which Account:
			<form id="accountTrans" action="trans.cgi" method="post">	
				<select name="accountTrans" />
				<option value="all">ALL ACCOUNTS</option>
					%s
				</select>
				<input type="submit" value="go" />
			</form>
		""" % str
		
		
		
		
		
elif form.has_key("accountDeposit") and form["accountDeposit"].value!="":
	try:
		amount=float(form["amount"].value)
	except:
		html="Error with the amount"
	else:
		returnCode=deposit(form["accountDeposit"].value,amount)
		if(returnCode>=0):
			html="Deposit Success. New Balance %s" % str(returnCode)
		else:
			html="Deposit failed"

elif form.has_key("accountWithdraw") and form["accountWithdraw"].value!="":
	try:
		amount=float(form["amount"].value)
	except:
		html="Error with the amount"
	else:
		returnCode=withdraw(form["accountWithdraw"].value,amount)
		if(returnCode>=0):
			html="Withdraw Success. New Balance %s" % str(returnCode)
		else:
			html="Withdraw failed"
			
elif form.has_key("accountTransfer1") and form["accountTransfer1"].value!="":
	if (form["accountTransfer1"].value==form["accountTransfer2"].value):
		html="Cannot transfer on same account"
	else:
		try:
			amount=float(form["amount"].value)
		except:
			html="Error with the amount"
		else:
			balance1=withdraw(form["accountTransfer1"].value,amount)
			if(balance1>=0):
				balance2=deposit(form["accountTransfer2"].value,amount)
				if (balance2>=0):
					html="Transfer successful. <br />Account %s new Balance: %s<br />Account %s new Balance: %s" % (form["accountTransfer1"].value,str(balance1),form["accountTransfer2"].value,str(balance2))
				else:
					#undo withdraw
					if(deposit(form["accountTransfer1"].value,amount)<0):
						html="ERROR: Account %s debited but Account %s could not be credited with %s" % (form["accountTransfer1"].value,form["accountTransfer2"].value,amount)
					html="Deposit failed. Operation failed safely"
			else:
				html="Withdraw failed"
				
elif form.has_key("accountTrans") and form["accountTrans"].value!="":
	if (form["accountTrans"].value=="all"):
		query="""
			SELECT transaction_id, date, amount, type, account_number
			FROM transaction
			ORDER BY date DESC
		"""
	else:
		query="""
			SELECT transaction_id, date, amount, type, account_number
			FROM transaction
			WHERE transaction.account_number='%s'
			ORDER BY date DESC
		""" % (form["accountTrans"].value)

	cursor.execute(query)
	rows = cursor.fetchall ()
	
	html="""
		<table border="1">
			<tr>
				<th>transaction_id</th>
				<th>date</th>
				<th>amount</th>
				<th>type</th>
				<th>account_number</th>
			</tr>
	"""
	
	for row in rows:
		html+="""
			<tr>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
			</tr>
		
		""" % (row[0], row[1], row[2], row[3], row[4])
		
	html+="</table>"	
	
	
	
print '<html><body><a href="/comp353/demo/">Home</a><br />'
print html
print "</html></body>"

#cursor.execute ("show tables;")
#rows = cursor.fetchall ()

#for row in rows:
#	print row

cursor.close ()
conn.close ()