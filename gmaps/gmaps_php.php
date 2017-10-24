<?php
	//https://developers.google.com/maps/documentation/javascript/mysql-to-maps#domxml
	
	$dom = new DOMDocument("1.0");
	$node = $dom->createElement("ap_list"); //Create new element node
	$parnode = $dom->appendChild($node); //make the node show up 

	$connect = mysqli_connect("localhost","root","");
	if(!$connect){
		die('Cant connect: '. mysqli_error());
	}
	
	$set_db = mysqli_select_db($connect,"gmaps");
	if(!$set_db){
		die('Cant use db: '. mysqli_error());
	}
	
	$query = "SELECT * FROM aps";
	$result = mysqli_query($connect, $query);
	if(!$result){
		die('Wrong query: '. mysqli_error());
	}
	
	//output XML
	header("Content-type: text/xml");
	
	while($row = mysqli_fetch_assoc($result)){
		$node = $dom->createElement("ap");
		$newnode = $parnode->appendChild($node);
		$newnode->setAttribute("id", $row['id']);
		$newnode->setAttribute("mac", $row['mac']);
		$newnode->setAttribute("ssid", $row['ssid']);
		$newnode->setAttribute("isp", $row['isp']);
		$newnode->setAttribute("lat", $row['lat']);
		$newnode->setAttribute("lng", $row['lng']);
	}
	
	echo $dom->saveXML();
	
?>