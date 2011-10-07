<?php
require_once 'db.php';

$db_server = new Database();
$db_server->Connect();

$query = "SELECT * FROM branch";
$result = mysql_query($query);

if(!$result) die("Database access failed: " . mysql_error());

$rows = mysql_num_rows($result);

echo 
"<table border='1'>
<tr>
<th>BranchID</th>
<th>Branch Name</th>
<th>Address</th>
<th>City</th>
<th>Phone</th>
<th>Fax</th>
<th>Opening Date</th>
<th>ManagerID</th>
</tr>
";
echo "<tr>";

for($i = 0; $i < $rows; ++$i) {

	echo "<td>" . mysql_result($result,$i,'branch_id') . "</td>";
	echo "<td>" . mysql_result($result,$i,'branch_name') . "</td>";
	echo "<td>" . mysql_result($result,$i,'address') . "</td>";
	echo "<td>" . mysql_result($result,$i,'city') . "</td>";
	echo "<td>" . mysql_result($result,$i,'phone') . "</td>";
	echo "<td>" . mysql_result($result,$i,'fax') . "</td>";
	echo "<td>" . mysql_result($result,$i,'opening_date') . "</td>";
	echo "<td>" . mysql_result($result,$i,'manager_id') . "</td>";
	echo "</tr><tr>";
}

echo "</table>";
?>
