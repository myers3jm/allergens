<head>
	<?php
		require 'common.php';
		require 'database.php';
	?>
</head>
<h2>Dunkin' Allergen Guide</h2>
<?php 
	echo "<p>The latest Dunkin' menu was fetched at $time_fetched on $date_fetched.</p>"
?>

<body>
	<p>This web application may not behave as expected from 11:59 PM to 12:01 AM, as that is when it attempts to update itself.</p>
	<form id="query-form" method="POST" action="index.php">
		<input id="query" type="text" name="query" for="query" placeholder="Product name">
		<br />
		<!-- <input id="gluten-box" class="restriction" type="checkbox" name="gluten_free" for="gluten_free">
		<label for="gluten-box">Gluten-free</label><br />
		<input id="dairy-box" class="restriction" type="checkbox" name="dairy_free" for="dairy_free">
		<label for="dairy-box">Dairy-free</label><br /> -->
		<button class="button" type="submit">Search</button>
	</form>

	<?php
		if (isset($_POST["query"]) || isset($_POST["gluten_free"]) || isset($_POST["dairy_free"])) {
	?>
	<table>
		<tr>
			<th>Product Name</th>
			<th>Allergens</th>
		</tr>

		<?php
			$conn = connect();
			$results = query_builder($conn, $_POST);
			if ($results) {
				foreach($results as $result) {
					echo "<tr><td>";
					echo $result['product_name'];
					echo "</td><td>";
					echo $result['allergens'];
					echo "</td></tr>";
				}
			}
		?>
	</table>
	
	
	<?php
		}
	?>
</body>
