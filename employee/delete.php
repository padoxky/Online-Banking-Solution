<?php
require_once '../db.php';

$db_server = new Database();
$db_server->Connect();

$sql="DELETE FROM employee WHERE employee_id='$_POST[employee_id]'";

if (!mysql_query($sql))
  {
  die('Error: ' . mysql_error());
  }
echo "1 record deleted";
$db_server->Close();
?>

