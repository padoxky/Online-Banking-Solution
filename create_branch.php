<?php
	if(isset($_POST['branch_name']) && isset($_POST['manager_id'])){
		$branch_name = $_POST['branch_name'];
		$manager_id = $_POST['manager_id'];
	}
	
	if(isset($_POST['address']))
		$address = $_POST['address'];
		
	if(isset($_POST['city']))
		$city = $_POST['city'];

	if(isset($_POST['phone']))
		$phone = $_POST['phone'];
		
	if(isset($_POST['fax']))
		$fax = $_POST['fax'];
		
	if(isset($_POST['opening_date']))
		$opening_date = $_POST['opening_date'];
			
	require_once 'db.php';
	
	$db_server = new Database();
	$db_server->Connect();

	if(isset($_POST['branch_name']) && isset($_POST['manager_id'])) {
		$query = "INSERT INTO branch VALUES" . "(NULL, '$branch_name', '$address', '$city', '$phone', '$fax', '$opening_date', '$manager_id')";
		
		$result = mysql_query($query);

	
	//putBranch($branch_id, $branch_name, $address, $city, $phone, $fax, $opening_date, $manager_id);
	//$query = "INSERT INTO branch ";
	//$result = mysql_query($query);
	
		if(!$result) 
			die("Database access failed: " . mysql_error());		
		else 
			echo "Branch created";	
	}
	$db_server->Close();
?>