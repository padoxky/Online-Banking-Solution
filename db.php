<?php

class Database {

	private $database_handler = false;
	
	public function Connect() {
		include("db_info.php");
		if ($this->database_handler)
			return;
		$this->database_handler = mysql_connect($db_hostname, $db_username, $db_password) or die("Unable to connect to MySQL: " . mysql_error());		
	
	
		mysql_select_db($db_database) or die("Cannot select database");
		return true;
	}
	
	public function Close() {
		if($this->database_handler)
			mysql_close($this->database_handler);
	}

	
}	
?>