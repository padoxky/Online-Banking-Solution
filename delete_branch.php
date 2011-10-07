<?php
	require_once 'db.php';
	
	if(isset($_POST['branch_id'])) {
		$branch_id = $_POST['branch_id'];
		
		$db = new Database();
		$db->Connect();
		
		$query = "DELETE FROM branch WHERE branch_id = '$branch_id'";
		$result = mysql_query($query);
	}	
	
	if(!$result) 
		die("Deletion failed" . mysql_error());
	else 
		echo "Delete successful";
?>