<?php
	$connect = mysqli_connect("localhost","root","");
	if(!$connect){
		die('Cant connect: '. mysqli_error($connect));
	}

	$set_db = mysqli_select_db($connect,"gmaps");
	if(!$set_db){
		die('Cant use db: '. mysqli_error($connect));
	}
	
	$myfile = fopen("trike_gps_readings.txt", "r") or die("Unable to open file!");
	while(!feof($myfile)) {
		$line = fgets($myfile);
		$array = explode(">>",$line);
		
		$datetime = explode(" ",$array[0]);
		$date = $datetime[0];
		$time = rtrim($datetime[1]);
		
		$coords = explode(",",$array[1]);
		$lat = trim($coords[0]);
		$lng = trim($coords[1]);
		echo "date:" .$date. ",time:" .$time. ",lat:" .$lat. ",lng:" .$lng. "<br>";
		
		$query = "INSERT INTO gps_readings (time,lat,lng) VALUES ('$time','$lat','$lng')";
		$result = mysqli_query($connect,$query);
		if (!$result) {
			die('Invalid query: ' . mysqli_error($connect));
		}
	}
	fclose($myfile);
?>