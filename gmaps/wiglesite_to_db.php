<?php
	$connect = mysqli_connect("localhost","root","");
	if(!$connect){
		die('Cant connect: '. mysqli_error($connect));
	}

	$set_db = mysqli_select_db($connect,"gmaps");
	if(!$set_db){
		die('Cant use db: '. mysqli_error($connect));
	}
	
	$myfile = fopen("teachersvill/parsed_wiglesite.txt", "r") or die("Unable to open file!");
	while(!feof($myfile)) {
		$line = fgets($myfile);
		$array = explode("|",$line);
		$ssid = $array[0];
		$ap_mac = $array[1];
		$coord = explode(",",$array[2]);
		$lat = $coord[0];
		$lng = rtrim($coord[1]);
		$rssi = 0;
		$channel = 0;
		echo $ap_mac ." with coordinates ". $lat ." and ". $lng .", RSSI is: ". $rssi .",Ch: ". $channel ."<br>";
		
		$query = "INSERT INTO aps (ssid,mac,channel,lat,lng,rssi,label) VALUES ('$ssid','$ap_mac','$channel','$lat','$lng','$rssi','wiglesite')";
		$result = mysqli_query($connect,$query);
		if (!$result) {
			die('Invalid query: ' . mysqli_error($connect));
		}
	}
	fclose($myfile);
?>