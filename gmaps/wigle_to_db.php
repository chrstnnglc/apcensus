<?php
	$connect = mysqli_connect("localhost","root","");
	if(!$connect){
		die('Cant connect: '. mysqli_error($connect));
	}

	$set_db = mysqli_select_db($connect,"gmaps");
	if(!$set_db){
		die('Cant use db: '. mysqli_error($connect));
	}
	
	$myfile = fopen("parsed_wigle.txt", "r") or die("Unable to open file!");
	while(!feof($myfile)) {
		$line = fgets($myfile);
		$array = explode("=",$line);
		$ap_mac = $array[0];
		$coord = explode(",",$array[1]);
		$lat = $coord[0];
		$lng = rtrim($coord[1]);
		$rssi = $array[2];
		$channel = rtrim($array[3]);
		echo $ap_mac ." with coordinates ". $lat ." and ". $lng .", RSSI is: ". $rssi .",Ch: ". $channel ."<br>";
		
		$query = "INSERT INTO aps (ssid,mac,channel,lat,lng,rssi,label) VALUES ('none','$ap_mac','$channel','$lat','$lng','$rssi','wigle')";
		$result = mysqli_query($connect,$query);
		if (!$result) {
			die('Invalid query: ' . mysqli_error($connect));
		}
	}
	fclose($myfile);
?>