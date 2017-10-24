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
  $newnode->setAttribute("isp", $row['isp']);
  $newnode->setAttribute("lat", $row['lat']);
  $newnode->setAttribute("lng", $row['lng']);
}

echo $dom->saveXML();


/*INSERTED VALUES

14.675143, 121.041914
14.675309, 121.042048
14.674671, 121.041904
14.674723, 121.041995
14.675081, 121.041464

'14.674910','121.041469'
'14.675024','121.041646'
'14.674754','121.041619'
'14.675044','121.041989'
INSERT INTO aps (ssid,mac,isp,lat,lng) VALUES ('test','00-00-00-00-00-00','pldc','14.675278','121.041727');   this is the 10th

*/


?>
