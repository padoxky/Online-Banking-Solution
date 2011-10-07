<?php
	require_once 'db.php';
	
	if(isset($_POST['branch_id']) && $_POST['branch_id'] != ""){
		$branch_id = $_POST['branch_id'];
		$db_server = new Database();
		$db_server->Connect();
		
		$isUpdated = false;
		
		if(isset($_POST['branch_name']) && ($_POST['branch_name']) != "") {
			$branch_name = $_POST['branch_name'];
			$query = "UPDATE branch SET branch_name = '$branch_name' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}
		
		if(isset($_POST['manager_id']) && ($_POST['manager_id']) != ""){
			$manager_id = $_POST['manager_id'];
			$query = "UPDATE branch SET manager_id = '$manager_id' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}
		
		if(isset($_POST['address']) && ($_POST['address']) != "") {
			$address = $_POST['address'];
			$query = "UPDATE branch SET address = '$address' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}	
		
		if(isset($_POST['city']) && ($_POST['city']) != "") {
			$city = $_POST['city'];
			$query = "UPDATE branch SET city = '$city' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}
		
		if(isset($_POST['phone']) && ($_POST['phone']) != "") {
			$phone = $_POST['phone'];
			$query = "UPDATE branch SET phone = '$phone' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}	
		
		if(isset($_POST['fax']) && ($_POST['fax']) != "") {
			$fax = $_POST['fax'];
			$query = "UPDATE branch SET fax = '$fax' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}
		
		if(isset($_POST['opening_date']) && ($_POST['opening_date']) != "") {
			$opening_date = $_POST['opening_date'];
			$query = "UPDATE branch SET opening_date = '$opening_date' WHERE branch_id = '$branch_id'";
			mysql_query($query);
			$isUpdated = true;
		}	
	}
	
	if(!$isUpdated) 
		die("Database access failed: " . mysql_error());		
	else 
		echo "Branch updated";	
	$db_server->Close();
?>