<?php
require_once '../db.php';
$db_server = new Database();
$db_server->Connect();

$branch_id = intval($_POST['branch_id']);
if ( $branch_id == 0 )
	{
	die('Error: Bad Branch ID' . mysql_error());
	}

$sql="UPDATE employee SET title='$_POST[title]', name='$_POST[name]', 
address='$_POST[address]', salary='$_POST[salary]', start_date='$_POST[start_date]', branch_id = $branch_id
WHERE employee_id ='$_POST[employee_id]'";

if (!mysql_query($sql))
  {
  die('Error: ' . mysql_error());
  }
echo "1 record updated";
$db_server->Close();
?>