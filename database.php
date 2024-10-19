<?php
    function connect() {
        $mysqli = new mysqli('localhost',
							 'dunkin_admin',
							 'TODO CHANGE ME',
							 'dunkin_allergens');
		if ($mysqli->connect_errno) {
			printf("Database connection failed: %s\n", $mysqli->connect_error);
			exit();
		}
        return $mysqli;
    }

	function query_builder($database_connection, $post) {
		$cmd = 'SELECT * FROM menu WHERE';
		// Add specified filters
		if (isset($post['query'])) {
			$cmd = $cmd . ' product_name LIKE CONCAT("%", ?, "%")';
			// Add AND if more to add to query
			if (isset($post['gluten_free']) || isset($post['dairy_free'])) {
				$cmd = $cmd . ' AND';
			}
		}
		// if (isset($post['gluten_free'])) {
		// 	$cmd = $cmd . ' LOWER(allergens) NOT LIKE \'%gluten%\'';
		// 	$cmd = $cmd . ' AND LOWER(allergens NOT LIKE \'%wheat%\'';
		// 	$cmd = $cmd . ' AND LOWER(allergens NOT LIKE \'%barley%\'';
		// 	// Add AND if more to add to query
		// 	if (isset($post['dairy_free'])) {
		// 		$cmd = $cmd . ' AND';
		// 	}
		// }
		// if (isset($post['dairy_free'])) {
		// 	$cmd = $cmd . ' LOWER(allergens) NOT LIKE \'%milk%\'';
		// 	$cmd = $cmd . ' AND LOWER(allergens NOT LIKE \'%dairy%\'';
		// }

		// Conclude prepared statement construction
		$cmd = $cmd . ';';

		// Prepare statement and execute
		$stmt = $database_connection->prepare($cmd);
		$stmt->bind_param('s', htmlentities(strtolower($post['query'])));
		$stmt->execute();
		$query_result = $stmt->get_result();
		return $query_result->fetch_all(mode: MYSQLI_ASSOC);
	}
?>