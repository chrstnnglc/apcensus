<?php
// Start XML file, create parent node
$dom = new DOMDocument("1.0");
$node = $dom->createElement("ap_list");
$parnode = $dom->appendChild($node);

$connect = mysqli_connect("localhost","root","");
	if(!$connect){
		die('Cant connect: '. mysqli_error());
	}

$set_db = mysqli_select_db($connect,"gmaps");
	if(!$set_db){
		die('Cant use db: '. mysqli_error());
	}

$query = "SELECT * FROM aps";
$result = mysqli_query($connect,$query);
if (!$result) {
  die('Invalid query: ' . mysqli_error());
}


//output XML
header("Content-type: text/xml");

// Iterate through the rows, adding XML nodes for each

while ($row = mysqli_fetch_assoc($result)){
  // Add to XML document node
  $node = $dom->createElement("ap");
  $newnode = $parnode->appendChild($node);
  $newnode->setAttribute("id",$row['id']);
  $newnode->setAttribute("ssid",$row['ssid']);
  $newnode->setAttribute("mac", $row['mac']);
  $newnode->setAttribute("channel", $row['channel']);
  $newnode->setAttribute("lat", $row['lat']);
  $newnode->setAttribute("lng", $row['lng']);
  $newnode->setAttribute("label", $row['label']);
}

echo $dom->saveXML();
?>
