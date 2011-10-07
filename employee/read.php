<?php
require_once '../db.php';
$db_server = new Database();
$db_server->Connect();

$branch_id = intval($_POST['branch_id']);
if ( $branch_id == 0 )
	{
	die('Error: Bad Branch ID' . mysql_error());
	}
	
$result = mysql_query("SELECT * FROM employee WHERE branch_id = $branch_id");

echo "<table border='1'>
<tr>
<th>EmployeeID</th>
<th>Title</th>
<th>Name</th>
<th>Address</th>
<th>Salary</th>
<th>StartDate</th>
<th>BranchID</th>
</tr>";

while($row = mysql_fetch_array($result))
  {
  echo "<tr>";
  echo "<td>" . $row['employee_id'] . "</td>";
  echo "<td>" . $row['title'] . "</td>";
  echo "<td>" . $row['name'] . "</td>";
  echo "<td>" . $row['address'] . "</td>";
  echo "<td>" . $row['salary'] . "</td>";
  echo "<td>" . $row['start_date'] . "</td>";
  echo "<td>" . $row['branch_id'] . "</td>";
  echo "</tr>";
  }
echo "</table>";

// list the rest of the employees without their salary
$result = mysql_query("SELECT * FROM employee WHERE branch_id <> $branch_id");

echo "<table border='1'>
<tr>
<th>EmployeeID</th>
<th>Title</th>
<th>Name</th>
<th>Address</th>
<th>StartDate</th>
<th>BranchID</th>
</tr>";

while($row = mysql_fetch_array($result))
  {
  echo "<tr>";
  echo "<td>" . $row['employee_id'] . "</td>";
  echo "<td>" . $row['title'] . "</td>";
  echo "<td>" . $row['name'] . "</td>";
  echo "<td>" . $row['address'] . "</td>";
//  echo "<td>" . $row['salary'] . "</td>";
  echo "<td>" . $row['start_date'] . "</td>";
  echo "<td>" . $row['branch_id'] . "</td>";
  echo "</tr>";
  }
echo "</table>";
$db_server->Close();
?>

