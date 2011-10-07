
<form method="post" action="<?php print $_SERVER['PHP_SELF']?>">
	
	
	<h2>Client ID: </h2><input type="text" name="read" />
	<input type="submit" value="GO" />
	
<?php
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
    }}

	echo "<p> Client name:[{$row['name']}] .  </p>";
	echo "<p> Address:[{$row['address']}] .  </p>";
	echo "<p> Date of birth:[{$row['dob']}] .  </p>";
	echo "<p> Joining date:[{$row['joining_date']}] .  </p>";
	echo "<p> Client ID:[{$row['client_id']}] .  </p>";

}
mysql_free_result($result);
?>

