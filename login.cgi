#!/usr/bin/python

# Required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

import cgi, MySQLdb
import cgitb; cgitb.enable() 

#load up the form
form=cgi.FieldStorage()

#create a db connection, place databass info here
try:
	conn = MySQLdb.connect (host = "",
				user = "",
				passwd = "",
				db = "")
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)
	
cursor = conn.cursor ()

if form.has_key("what") and form["what"].value!="" and form.has_key("id") and form["id"].value!="":
	what=form["what"].value
	id=form["id"].value
	if(form.has_key("password") and form["password"].value!=""):
		password=form["password"].value
	else: 
		password=""
	
	
	if what=="c":
		query="""
			SELECT client_id, client.password
			FROM client
			WHERE client_id='%s' AND client.password='%s'
		""" % (id,password)
			
		cursor.execute(query)
		row=cursor.fetchone()
		
		if (row):
			#####################
			#query accounts belonging to client
			#####################
			query="""
					SELECT account_number, account.client_id, client.name, balance
					FROM account, client
					WHERE account.client_id=client.client_id AND client.client_id='%s'
					ORDER BY account_number
				""" % id
			cursor.execute (query)
			rows = cursor.fetchall ()
			
			#build options
			str=""
			for row in rows:
				str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
			
			#################
			#query all accounts
			##################
			query="""
					SELECT account_number, account.client_id, client.name, balance
					FROM account, client
					WHERE account.client_id=client.client_id
					ORDER BY account_number
				"""
			cursor.execute (query)
			rows = cursor.fetchall ()
			
			#build options
			str2=""
			for row in rows:
				str2+='<option value="%s">Account: %s, Owner: %s</option>' % (row[0],row[0], row[2])
			
			
			#################
			#html
			##################			
			html="""
				<h2>Branch CRUD Actions</h2>
				<ol>
					<li><a href="read_branch.php">Read All Branch Information</a></li>
				</ol>
				<h2>Client CRUD Actions</h2>
				<ol>
					<li>
						<form method="post" action="readclient.php">
						<input type="hidden" name="read" value="%s"/>
						<input type="submit" value="Read your client info" />
						</form>
					</li>
				</ol>
				<h2>Account CRUD Actions</h2>
				<ol>				
					<li>
						Select one of your accounts to get its info:
						<form id="accountRead" action="account.cgi" method="post">	
							<select name="accountRead" />
								%s
							</select>

							<input type="submit" value="Read Account" />
						</form> 
					</li>
				</ol>
				<h2>Transaction CRUD Actions</h2>
				<ol>				
					<li>
						Select Account & Specify Amount to Withdraw
						<form id="accountWithdraw" action="trans.cgi" method="post">	
							<select name="accountWithdraw" />
								%s
							</select>
							Amount:<input type="text" name="amount" value="0" />
							<input type="submit" value="Withdraw" />
						</form>
					</li>
					<li>
						Select Account & Specify Amount to Deposit
						<form id="accountDeposit" action="trans.cgi" method="post">	
							<select name="accountDeposit" />
								%s
							</select>
							Amount:<input type="text" name="amount" value="0" />
							<input type="submit" value="Deposit" />
						</form>
					</li>
					<li>
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
							<input type="submit" value="Transfer" />
						</form>
					</li>
					<li>
						Select one of your accounts to Query its Transactions:
						<form id="accountTrans" action="trans.cgi" method="post">	
							<select name="accountTrans" />
							<option value="all">ALL ACCOUNTS</option>
								%s
							</select>
							<input type="submit" value="go" />
						</form>
					</li>
				</ol>
			""" % (id,str,str,str,str,str2,str)
		else:
			html="Incorrect id/password combination"
		
	elif what=="t":
		query="""
			SELECT employee_id, password
			FROM employee
			WHERE employee_id='%s' AND password='%s'
		""" % (id, password)
		
		cursor.execute(query)
		row=cursor.fetchone()
		
		if (row):
			#################
			#query all accounts
			##################
			query="""
					SELECT account_number, account.client_id, client.name, balance
					FROM account, client
					WHERE account.client_id=client.client_id
					ORDER BY account_number
				"""
			cursor.execute (query)
			rows = cursor.fetchall ()
			
			#build options
			str=""
			for row in rows:
				str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
			
			
			#################
			#html
			##################			
			html="""
				<h2>Branch CRUD Actions</h2>
				<ol>
					<li><a href="read_branch.php">Read All Branch Information</a></li>
				</ol>
				<h2>Client CRUD Actions</h2>
				<ol>
					<li>
						<form id="actionForm" action="addclient.php" method="post">	
							<input type="submit" value="Add a new client" />
						</form>
					</li>
					<li>
						<form id="actionForm" action="updateclient.php" method="post">	
							<input type="submit" value="Update client information" />
						</form>
					</li>
					<li>
						<form id="actionForm" action="readclient.php" method="post">	
							<input type="submit" value="Read client information" />
						</form>
					</li>
				</ol>
				<h2>Employee CRUD Actions</h2>
				<ol>
					<li>
						<a href="read_employee.html">List Employees</a>
					</li>
				</ol>
				<h2>Account CRUD Actions</h2>
				<ol>
					<li>
						Select Account Action
						<form id="actionForm" action="account.cgi" method="post">	
							
							<select name="action" />
								<option value="default"></option>
								<option value="c">Create Account</option>
								<option value="r">Read Account</option>
								<option value="u">Update Account</option>
							</select>

							<input type="submit" value="go" />
						</form>
					</li>
				</ol>
				<h2>Transaction CRUD Actions</h2>
				<ol>
					<li>
						Select Account & Specify Amount to Withdraw
						<form id="accountWithdraw" action="trans.cgi" method="post">	
							<select name="accountWithdraw" />
								%s
							</select>
							Amount:<input type="text" name="amount" value="0" />
							<input type="submit" value="Withdraw" />
						</form>
					</li>
					<li>
						Select Account & Specify Amount to Deposit
						<form id="accountDeposit" action="trans.cgi" method="post">	
							<select name="accountDeposit" />
								%s
							</select>
							Amount:<input type="text" name="amount" value="0" />
							<input type="submit" value="Deposit" />
						</form>
					</li>
					<li>
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
							<input type="submit" value="Transfer" />
						</form>
					</li>
					<li>
						Select Account to Query Transactions:
						<form id="accountTrans" action="trans.cgi" method="post">	
							<select name="accountTrans" />
							<option value="all">ALL ACCOUNTS</option>
								%s
							</select>
							<input type="submit" value="go" />
						</form>
					</li>
				</ol>
			""" % (str,str,str,str,str)
		else:
			html="Incorrect id/password combination"
	
	elif what=="m":
		query="""
			SELECT employee_id, password
			FROM employee
			WHERE employee_id='%s' AND password='%s'
		""" % (id, password)
		
		cursor.execute(query)
		row=cursor.fetchone()
		
		if (row):
			#make sure its a manager
			query="""
				SELECT branch_id, manager_id
				FROM branch
				WHERE manager_id='%s'
			""" % id
			
			cursor.execute(query)
			row2=cursor.fetchone()
						
			if (row2):
				branch=row2[0]
				#################
				#query all accounts
				##################
				query="""
						SELECT account_number, account.client_id, client.name, balance
						FROM account, client
						WHERE account.client_id=client.client_id
						ORDER BY account_number
				"""
				cursor.execute (query)
				rows = cursor.fetchall ()
				
				#build options
				str=""
				for row in rows:
					str+='<option value="%s">Account: %s, Owner: %s, Balance: %s</option>' % (row[0],row[0], row[2], row[3])
				
				
				#################
				#html
				##################			
				html="""
					<h2>Branch CRUD Actions</h2>
					<ol>
						<li><a href="read_branch.php">Read All Branch Information</a></li>
						<li><a href="create_branch.html">Create Branch</a></li>
						<li><a href="update_branch.html">Update Branch</a></li>
						<li><a href="delete_branch.html">Delete Branch</a></li>
					</ol>
					<h2>Client CRUD Actions</h2>
					<ol>
					<li>
						<form id="actionForm" action="addclient.php" method="post">	
							<input type="submit" value="Add a new client" />
						</form>
					</li>
					<li>
						<form id="actionForm" action="updateclient.php" method="post">	
							<input type="submit" value="Update client information" />
						</form>
					</li>
					<li>
						<form id="actionForm" action="readclient.php" method="post">	
							<input type="submit" value="Read client information" />
						</form>
					</li>
					<li>
						<form id="actionForm" action="deleteclient.php" method="post">	
							<input type="submit" value="Delete client" />
						</form>
					</li>
					</ol>
					<h2>Employee CRUD Actions</h2>
					<ol>
						<li><a href="read_employee.html">List Employees</a></li>
						<li><a href="delete_employee.html">Delete Employee</a></li>
						<li><a href="create_employee.html">Insert Employee</a></li>
						<li><a href="update_employee.html">Update Employee Info</a></li>
					</ol>
					<h2>Account CRUD Actions</h2>
					<ol>
						<li>
							Select Account Action
							<form id="actionForm" action="account.cgi" method="post">	
								
								<select name="action" />
									<option value="default"></option>
									<option value="c">Create Account</option>
									<option value="r">Read Account</option>
									<option value="u">Update Account</option>
								</select>

								<input type="submit" value="go" />
							</form>
						</li>
					</ol>
					<h2>Transaction CRUD Actions</h2>
					<ol>
						<li>
							Select Account & Specify Amount to Withdraw
							<form id="accountWithdraw" action="trans.cgi" method="post">	
								<select name="accountWithdraw" />
									%s
								</select>
								Amount:<input type="text" name="amount" value="0" />
								<input type="submit" value="Withdraw" />
							</form>
						</li>
						<li>
							Select Account & Specify Amount to Deposit
							<form id="accountDeposit" action="trans.cgi" method="post">	
								<select name="accountDeposit" />
									%s
								</select>
								Amount:<input type="text" name="amount" value="0" />
								<input type="submit" value="Deposit" />
							</form>
						</li>
						<li>
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
								<input type="submit" value="Transfer" />
							</form>
						</li>
						<li>
							Select Account to Query Transactions:
							<form id="accountTrans" action="trans.cgi" method="post">	
								<select name="accountTrans" />
								<option value="all">ALL ACCOUNTS</option>
									%s
								</select>
								<input type="submit" value="go" />
							</form>
						</li>
					</ol>
				""" % (str,str,str,str,str)
			else:
				html="This employee is not a manager"
		else:
			html="Incorrect id/password combination"

	else:
		html="what are you"
else:
	html="missing what or id"
	

print '<html><body><a href="/comp353/demo/">Login</a><br />'
print html
print "</html></body>"

#cursor.execute ("show tables;")
#rows = cursor.fetchall ()

#for row in rows:
#	print row

cursor.close ()
conn.close ()

