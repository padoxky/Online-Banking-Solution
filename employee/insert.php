<?php
require_once '../db.php';
$db_server = new Database();
$db_server->Connect();
  
$branch_id = intval($_POST['branch_id']);
if ( $branch_id == 0 )
	{
	die('Error: Bad Branch ID' . mysql_error());
	}
$sql = "INSERT INTO  `bankc35320110808`.`employee` (
`title` , `name` , `address` , `salary`, `start_date`, `branch_id`)
VALUES ('$_POST[title]','$_POST[name]','$_POST[address]','$_POST[salary]', 
'$_POST[start_date]', $branch_id)";
  
if (!mysql_query($sql))
  {
  die('Error: ' . mysql_error());
  }
echo "1 record added";
$db_server->Close();
?>