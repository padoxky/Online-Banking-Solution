
<form method="post" action="<?php print $_SERVER['PHP_SELF']?>">
	
	
	<p>Insert client ID: <input type="text" name="read" />
	<input type="submit" value="Search" /></p>
	
<?php
	global $name;
	global $ID;
	global $address;
	global $dob;
	global $join;


$link = mysql_connect('bankc35320110808.db.7939020.hostedresource.com', 'bankc35320110808','comP353');
if (!$link) {
    die('Could not connect: ' . mysql_error());
}
$db_selected = mysql_select_db('bankc35320110808');
if (!$db_selected) {
    die('Could not select database: ' . mysql_error());
}
$query = 'SELECT client_id FROM client';
$result = mysql_query($query);
if (!$result) {
    die('Query failed: ' . mysql_error());
}




if ( isset(  $_POST['read'] ) ) {
	

	$query1 = "SELECT * FROM client WHERE client_id = '{$_POST['read']}'";
	$result1 = mysql_query($query1);
	if (!$result1) {
    	die('Query failed: ' . mysql_error());
	}
	/* fetch rows in reverse order */
	for ($i = mysql_num_rows($result1) - 1; $i >= 0; $i--) {
    	if (!mysql_data_seek($result1, $i)) {
        echo "Cannot seek to row $i: " . mysql_error() . "\n";
        continue;
    }

    if (!($row = mysql_fetch_assoc($result1))) {
        continue;
	
    	}
	$name= $row['name'];
	$address= $row['address'];
	$dob= $row['dob'];
	$join= $row['joining_date'];
	$ID= $row['client_id'];
	
	}
if ( isset( $_POST['submit'] ) ) {

	$name = $_POST['name'];
	$address = $_POST['address'];
	$dob = $_POST['dob'];
	$join = $_POST['join'];
	$ID = $_POST['id'];
	
	$query3 = "UPDATE client SET name = '$name', address = '$address', dob = '$dob', joining_date = '$join'  WHERE client_id = $ID";
	$result3 = mysql_query($query3);
	
	if (!$result3) {
    	die('Query failed: ' . mysql_error());
	}
	
	

}

}	
	
	


mysql_free_result($result);

?>

<h2><?php echo 'Client information:'; ?></h2>

<HTML><BODY><p>Name: <input type="text" name="name" value= "<?php echo $name; ?>" /></p></BODY></HTML>
<HTML><BODY><p>Address: <input type="text" name="address" value= "<?php echo $address; ?>" /></p></BODY></HTML>
<HTML><BODY><p>Date of birth: <input type="text" name="dob" value= "<?php echo $dob; ?>" /></p></BODY></HTML>
<HTML><BODY><p>Joining date: <input type="text" name="join" value= "<?php echo $join; ?>" /></p></BODY></HTML>
<HTML><BODY><p>ID number: <?php echo $ID; ?><input type = "hidden" name="id" value= "<?php echo $ID; ?>" /></p></BODY></HTML>

<HTML><BODY><p><form method="post" action="<?php print $_SERVER['PHP_SELF']?>"></p></BODY></HTML>
	
	<input name= "submit" type="submit" value="Submit" /></p></BODY></HTML>

	
