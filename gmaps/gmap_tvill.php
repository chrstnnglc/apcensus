<!DOCTYPE html >
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <title>AP Census Balara-TODA</title>
	
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
	  #selection_buttons {
		text-align: center;
		background-color: rgb(209,202,206);
		border: 3px solid black;
		padding: 25px 0 25px 0;
		margin-bottom: 10px;
	  }
	  .buttons{
		  height: 30px;
		  font-size: 15px;
		  margin: 0 15px 0 15px;
		  border: 2px solid black;
	  }
	  .buttons:hover{
		  cursor: pointer
	  }
	  .active{
		  font-weight: bold;
	  }
	  .inactive{
		  font-weight: normal;
		  opacity: 0.7
	  }
	  #ws_button{
		background-color: rgb(30,186,16);
	  }
	  #rp_button{
		 background-color: rgb(227,56,34); 
	  }
	  #rpc1_button{
		 background-color: violet; 
	  }
	  #rpc2_button{
		 background-color: orange; 
	  }
	  #w_button{
		background-color: rgb(58,111,237);
	  }
	  #time_button{
		 background-color: rgb(255,252,60); 
	  }
	  #speed_button{
		 background-color: green; 
	  }
	  #legend_cont{
		font-family: Arial, sans-serif;
        background: #FFF;
        padding: 10px;
        margin: 10px;
        border: 3px solid #000;
	  }
	  #legend_cont h2{
		  text-align: center;
		  margin: 0 0 10px 0;
	  }
	  #aps_legend{
		font-size: 15px;
	  }
	  #aps_legend p{
		  margin: 10px;
	  }
	  #legend_cont h3{
		  margin: 0 0 10px 0;
	  }
	  #grid_legend_table_ap, #grid_legend_table_time, #grid_legend_table_speed{
		font-size: 15px;
	  }
	  #grid_legend_table_time, #grid_legend_table_speed{
		  display: none;
	  }
	  .grid_legend{
		  height: 25px;
		  width: 25px;
		  border: 1px solid black;
	  }
	  .most_ap{
		background-color: #FF0000;
	  }
	  .more_ap{
		 background-color: #FA8072;  
	  }
	  .less_ap{
		 background-color: #F88379; 
	  }
	  .lesser_ap{
		 background-color: #FF91A4; 
	  }
	  .least_ap{
		 background-color: #FFC0CB; 
	  }
	  
	  .most_time{
		background-color: #A98600;
	  }
	  .more_time{
		 background-color: #E0B300;  
	  }
	  .lesser_time{
		 background-color: #E9D700; 
	  }
	  .least_time{
		 background-color: #FFF9AE; 
	  }
	  .most_speed{
		background-color: #163317;
	  }
	  .more_speed{
		 background-color: #214D22;  
	  }
	  .lesser_speed{
		 background-color: #47A64A; 
	  }
	  .least_speed{
		 background-color: #80FF84; 
	  }
    </style>
  </head>

  <body>
    <div id="map"></div>
	
	<div id="legend_cont">
		<h2>Legend</h2>
		<div id="aps_legend">
			<p> <img src="rp_marker.png"> &nbsp RasPi detected APs </p>
			<p> <img src="w_marker.png"> &nbsp WiGLE detected APs </p>
			<p> <img src="ws_marker.png"> &nbsp WiGLE Database APs </p>
			<p> <img src="rpc1_marker.jpeg"> &nbsp RPi 1-13 Channel </p>
			<p> <img src="rpc2_marker.png"> &nbsp RPi 1,6,11 Channel </p>
		</div>
		<h3> Grid Colors </h3>
		<table id="grid_legend_table_ap">
			<tr>
				<td><div class="grid_legend most_ap"></div></td>
				<td>More than 20 APs</td>
			</tr>
			<tr>
				<td><div class="grid_legend more_ap"></div></td>
				<td>15 to 20 APs</td>
			</tr>
			<tr>
				<td><div class="grid_legend less_ap"></div></td>
				<td>10 to 15 APs</td>
			</tr>
			<tr>
				<td><div class="grid_legend lesser_ap"></div></td>
				<td>5 to 10 APs</td>
			</tr>
			<tr>
				<td><div class="grid_legend least_ap"></div></td>
				<td>0 to 5 APs</td>
			</tr>
			<tr>
				<td><div class="grid_legend none"></div></td>
				<td>No data</td>
			</tr>
		</table>

		<table id="grid_legend_table_time">
			<tr>
				<td><div class="grid_legend most_time"></div></td>
				<td>More than 60 sec</td>
			</tr>
			<tr>
				<td><div class="grid_legend more_time"></div></td>
				<td>40 to 60 sec</td>
			</tr>
			<tr>
				<td><div class="grid_legend lesser_time"></div></td>
				<td>20 to 40 sec</td>
			</tr>
			<tr>
				<td><div class="grid_legend least_time"></div></td>
				<td>0 to 20 sec</td>
			</tr>
			<tr>
				<td><div class="grid_legend none"></div></td>
				<td>No data</td>
			</tr>
		</table>
		
		<table id="grid_legend_table_speed">
			<tr>
				<td><div class="grid_legend most_speed"></div></td>
				<td>More than 10 m/s</td>
			</tr>
			<tr>
				<td><div class="grid_legend more_speed"></div></td>
				<td>6 to 10 m/s</td>
			</tr>
			<tr>
				<td><div class="grid_legend lesser_speed"></div></td>
				<td>2 to 6 m/s</td>
			</tr>
			<tr>
				<td><div class="grid_legend least_speed"></div></td>
				<td>0 to 2 m/s</td>
			</tr>
			<tr>
				<td><div class="grid_legend none"></div></td>
				<td>No data</td>
			</tr>
		</table>
	</div>
	
	<div id="selection_buttons">
		<input onclick="toggleWS()" type="button" value="Wigle Site" id="ws_button" class="buttons active">
		<input onclick="toggleRP()" type="button" value="RasPi" id="rp_button" class="buttons active">
		<input onclick="toggleRPC1()" type="button" value="1-13" id="rpc1_button" class="buttons active">
		<input onclick="toggleRPC2()" type="button" value="1,6,11" id="rpc2_button" class="buttons active">
		<input onclick="toggleW()" type="button" value="Wigle" id="w_button" class="buttons active">
		<input onclick="toggleTime()" type="button" value="Time Spent" id="time_button" class="buttons inactive">
		<input onclick="toggleSpeed()" type="button" value="Speed" id="speed_button" class="buttons inactive">
		<span style="font-size: 20px;">|</span>
		<input onclick="getWDBtxt()" type="button" value="Filter Wigle DB" id="output_button" class="buttons active">
	</div>

<script>
var ws_markers = [];
var rp_markers = [];
var rpc1_markers = [];
var rpc2_markers = [];
var w_markers = [];
var rectArr = [];
var ws_lat = [];
var ws_lng = [];
var rp_lat = [];
var rp_lng = [];
var rpc1_lat = [];
var rpc1_lng = [];
var rpc2_lat = [];
var rpc2_lng = [];
var w_lat = [];
var w_lng = [];
var rpCountArr = [];
var rpc1CountArr = [];
var rpc2CountArr = [];
var wCountArr = [];
var wsCountArr = [];
var rectCountArr = [];
var rectTimeArr = [];
var rectSpeedArr = [];
var gps_lat = [];
var gps_lng = [];
var gps_timeArr = [];
var has_readings = [];
var ws_macs = [];
var map, rp_count, w_count, ws_count, rect_count, total_count;

function gridMap() { 
	map = new google.maps.Map(document.getElementById('map'), 
		{ 
			zoom: 17,
			center: {lat: 14.648441, lng: 121.059002},		
			mapTypeId: 'terrain',
			zoomControl: false
		}
	);
	//initialize infoWindow
	var infoWindow = new google.maps.InfoWindow;

	downloadUrl('test_g_fetch.php', function(data) {
		var xml = data.responseXML;
		var ap_list = xml.documentElement.getElementsByTagName('ap');
		//read elements of XML output
		Array.prototype.forEach.call(ap_list, function(ap) {
			var id = ap.getAttribute('id');
			var ssid = ap.getAttribute('ssid');
			var mac = ap.getAttribute('mac');
			var channel = ap.getAttribute('channel');
			var label = ap.getAttribute('label');
			var point = new google.maps.LatLng(
				parseFloat(ap.getAttribute('lat')),
				parseFloat(ap.getAttribute('lng'))
			);
			
			//set coordinates of marker to array respectively
			if (label == "rpi"){
				rp_lat.push(parseFloat(ap.getAttribute('lat')));
				rp_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			else if (label == "rpi113"){
				rpc1_lat.push(parseFloat(ap.getAttribute('lat')));
				rpc1_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			else if (label == "rpi1611"){
				rpc2_lat.push(parseFloat(ap.getAttribute('lat')));
				rpc2_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			else if (label == "wigle"){
				w_lat.push(parseFloat(ap.getAttribute('lat')));
				w_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			else if (label == "wiglesite"){
				ws_lat.push(parseFloat(ap.getAttribute('lat')));
				ws_lng.push(parseFloat(ap.getAttribute('lng')));
				ws_macs.push(mac);
			}
			//set the content of the infoWindow
			var infowincontent = document.createElement('div');
			var strong = document.createElement('strong');
			strong.textContent = ssid
			infowincontent.appendChild(strong);
			infowincontent.appendChild(document.createElement('br'));
	  
			mac = "MAC: " + mac;
			channel = "Ch: " + channel;
			var text = document.createElement('text');
			text.textContent = mac
			infowincontent.appendChild(text);
			infowincontent.appendChild(document.createElement('br'));
			var text = document.createElement('text');
			text.textContent = channel
			infowincontent.appendChild(text);
			
			
			//set color of legend
			if (label == "rpi"){
				icon = 'rp_marker.png'
			}
			else if (label == "rpi113"){
				icon = 'rpc1_marker.jpeg'
			}
			else if (label == "rpi1611"){
				icon = 'rpc2_marker.png'
			}
			else if (label == "wigle"){
				icon = 'w_marker.png'
			}
			else if (label == "wiglesite"){
				icon = 'ws_marker.png'
			}
			//create marker
			var marker = new google.maps.Marker({
				map: map,
				position: point,
				icon: icon
			});
			//assign corresponding markers to array
			if (label == "rpi"){
				rp_markers.push(marker)
			}
			else if (label == "rpi113"){
				rpc1_markers.push(marker)
			}
			else if (label == "rpi1611"){
				rpc2_markers.push(marker)
			}
			else if (label == "wigle"){
				w_markers.push(marker)
			}
			else if (label == "wiglesite"){
				ws_markers.push(marker)
			}
			
			//show the info on mouse hover
			marker.addListener('mouseover', function() {
				infoWindow.setContent(infowincontent);
				infoWindow.open(map, marker);
			});
	  
			//hide info when mouse leaves the marker
			marker.addListener('mouseout', function() {
				infoWindow.setContent(infowincontent);
				infoWindow.close(map, marker);
			});
		});
		
		//get the gps readings
		var gps_list = xml.documentElement.getElementsByTagName('gps');
		Array.prototype.forEach.call(gps_list, function(gps) {
			var time = gps.getAttribute('time');
			var id = gps.getAttribute('id');
			time = time.split(":");
			var gps_time = new Date();
			gps_time.setHours(+time[0]);
			gps_time.setMinutes(time[1]);
			gps_time.setSeconds(time[2]);
			gps_timeArr.push(gps_time);
			gps_lat.push(parseFloat(gps.getAttribute('lat')));
			gps_lng.push(parseFloat(gps.getAttribute('lng')));
		
		});

		var north = 14.651518;
		var south = LatCoordDistance(north,50);
		var west = 121.052077;
		var east = LngCoordDistance(north,west,50);
		
		var rectangle;
		total_count = 0;
		for(j=0; j < 13; j++){
			if(j==0){
				//do nothing
			}
			else{
				north = south;
				south = LatCoordDistance(north,50);//south = +((north - 0.000453).toFixed(6));
				west = 121.052077;;	//set the value of this equal to the initial west bound
				var east = LngCoordDistance(north,west,50);
			}
			for(i=0; i < 27; i++){
				if(i==0){
					//do nothing
				}
				else{
					west = east;
					east = LngCoordDistance(north,west,50); //east = +((west + 0.000453).toFixed(6));
				} 
				rectangle = new google.maps.Rectangle({ 
					strokeColor: '#000000', 
					strokeOpacity: 0.8, 
					strokeWeight: 1, 
					fillColor: '#000000', 
					fillOpacity: 0.0,  
					map: map, 
					bounds: { 
						north: north, 
						south: south, 
						east: east, 
						west: west  
					} 
				});
				
				//loop through all of our points and check whether it is inside this grid/rectangle being drawn
				rp_count = 0;
				rpc1_count = 0;
				rpc2_count = 0;
				w_count = 0;
				ws_count = 0;
				rect_count = 0;
				for(x = 0; x < rp_lat.length; x++){
					var point = new google.maps.LatLng(rp_lat[x], rp_lng[x]);
					if(rectangle.getBounds().contains(point)){
						rp_count++;
					}
				}
				for(x = 0; x < rpc1_lat.length; x++){
					var point = new google.maps.LatLng(rpc1_lat[x], rpc1_lng[x]);
					if(rectangle.getBounds().contains(point)){
						rpc1_count++;
					}
				}
				for(x = 0; x < rpc2_lat.length; x++){
					var point = new google.maps.LatLng(rpc2_lat[x], rpc2_lng[x]);
					if(rectangle.getBounds().contains(point)){
						rpc2_count++;
					}
				}
				for(x = 0; x < w_lat.length; x++){
					var point = new google.maps.LatLng(w_lat[x], w_lng[x]);
					if(rectangle.getBounds().contains(point)){
						w_count++;
					}
				}
				for(x = 0; x < ws_lat.length; x++){
					var point = new google.maps.LatLng(ws_lat[x], ws_lng[x]);
					if(rectangle.getBounds().contains(point)){
						ws_count++;
					}
				}
				rect_count = rp_count + rpc1_count + rpc2_count + w_count + ws_count;
				if (rect_count != 0){
					if(rect_count > 20){
						color = "#FF0000";
					}
					else if(rect_count > 15 && rect_count <= 20){
						color = "#FA8072";
					}
					else if(rect_count > 10 && rect_count <= 15){
						color = "#F88379";
					}
					else if(rect_count > 5 && rect_count <= 10){
						color = "#FF91A4";
					}
					else if(rect_count > 0 && rect_count <= 5){
						color = "#FFC0CB";
					}
					rectangle.setOptions({
						fillColor: color,
						fillOpacity: 0.9
					});
				}
				rectArr.push(rectangle);
				rpCountArr.push(rp_count);
				rpc1CountArr.push(rpc1_count);
				rpc2CountArr.push(rpc2_count);
				wCountArr.push(w_count);
				wsCountArr.push(ws_count);
				rectCountArr.push(String(rect_count));
				total_count = total_count + rect_count;
				rectTimeArr.push(0);
				rectSpeedArr.push(0);
			}
		}
		console.log(south);
		console.log(east);
		console.log("Total Count: " + total_count);
		
		//count how many seconds did we stay inside the rectangle
		for(i = 0; i < rectArr.length; i++){
			first_time = 0
			gps_readings = 0
			for(x = 0; x < gps_lat.length; x++){
				var point = new google.maps.LatLng(gps_lat[x], gps_lng[x]);
				if(rectArr[i].getBounds().contains(point)){
					if(first_time == 0){
						start = gps_timeArr[x];
						first_time = 1;
						gps_readings = 1;
						if(i==80){
							console.log("Start: " + start);
						}
						start_point = point;
					}
				}
				else{
					//if there was a previous gps reading in this box
					if(first_time == 1){
						time_spent = parseInt((gps_timeArr[x] - start)/1000);
						if(i==80){
							console.log("End: " + gps_timeArr[x]);
							console.log("Time: " + time_spent);
						}
						rectTimeArr[i] += time_spent;
						first_time = 0;
						end_point = point
						
						//compute for the speed
						var distance = google.maps.geometry.spherical.computeDistanceBetween(start_point, end_point);
						speed = distance / time_spent;
						rectSpeedArr[i] += speed;
					}
				}
			}
			has_readings.push(gps_readings);
		}
		//add event listners for each rectangle and get the count in that rectangle
		for(i = 0; i < rectArr.length; i++){
			google.maps.event.addListener(rectArr[i],'click', function(event) {
				for(j = 0; j < rectArr.length; j++){
					if(rectArr[j].getBounds().contains(event.latLng)){
						rect_count = rectCountArr[j];
						rect_time = rectTimeArr[j];
						rect_speed = rectSpeedArr[j];
					}
				}
				infoWindow.setContent("# of APs: <b>" + String(rect_count) + "</b> <br> Time Spent: <b>" + String(rect_time) + " seconds </b> <br> Speed: <b>" + String(rect_speed) + " m/s </b>")
				infoWindow.setPosition(event.latLng);
				infoWindow.open(map);
			}); 
		}
	});
	
	//add the list of legend, and toggle buttons in the map
	map.controls[google.maps.ControlPosition.RIGHT_TOP].push(document.getElementById('legend_cont'));
	map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(document.getElementById('selection_buttons'));
	
}

function countRectAP(){
	total_count = 0;
	for(i = 0; i < rectArr.length; i++){
		//loop through all of our points and check whether it is inside this grid/rectangle being drawn
		rect_count = 0;
		if(document.getElementById("rp_button").classList.contains("active")){
			rect_count = rect_count + rpCountArr[i]
		}
		if(document.getElementById("w_button").classList.contains("active")){
			rect_count = rect_count + wCountArr[i]
		}
		if(document.getElementById("ws_button").classList.contains("active")){
			rect_count = rect_count + wsCountArr[i]
		}
		if(rect_count != 0){
			if(rect_count > 20){
				color = "#FF0000";
			}
			else if(rect_count > 15 && rect_count <= 20){
				color = "#FA8072";
			}
			else if(rect_count > 10 && rect_count <= 15){
				color = "#F88379";
			}
			else if(rect_count > 5 && rect_count <= 10){
				color = "#FF91A4";
			}
			else if(rect_count > 0 && rect_count <= 5){
				color = "#FFC0CB";
			}
			rectArr[i].setOptions({
				fillColor: color,
				fillOpacity: 0.9
			});
		}
		else if (rect_count == 0){
			rectArr[i].setOptions({
				fillColor: "#000000",  //any color will do as long as transparent
				fillOpacity: 0.0
			});
		}
		rectCountArr[i] = String(rect_count);
		total_count = total_count + rect_count
	}
	console.log("Total Count: " + total_count)
}

function countRectTime(){
	for(i = 0; i < rectArr.length; i++){
		rect_time = rectTimeArr[i]
		if(rect_time != 0){
			//    !!!!!!!     change the values to higher times next time     !!!!!!!!!!!!!!
			if(rect_time > 60){
				color = "#A98600"
			}
			else if(rect_time > 40 && rect_time <= 60){
				color = "#E0B300"
			}
			else if(rect_time > 20 && rect_time <= 40){
				color = "#E9D700"
			}
			else if(rect_time > 0 && rect_time <= 20){
				color = "#FFF9AE"
			}
			rectArr[i].setOptions({
				fillColor: color,
				fillOpacity: 0.9
			});
		}
		else if(rect_time == 0){
			rectArr[i].setOptions({
				fillColor: "#000000",  //any color will do as long as transparent
				fillOpacity: 0.0
			});
		}
	}
}

function countRectSpeed(){
	for(i = 0; i < rectArr.length; i++){
		rect_speed = rectSpeedArr[i]
		if(rect_speed != 0){
			//    !!!!!!!     change the values to higher times next time     !!!!!!!!!!!!!!
			if(rect_speed > 10){
				color = "#163317"
			}
			else if(rect_speed > 6 && rect_speed <= 10){
				color = "#214D22"
			}
			else if(rect_speed > 2 && rect_speed <= 6){
				color = "#47A64A"
			}
			else if(rect_speed > 0 && rect_speed <= 2){
				color = "#80FF84"
			}
			rectArr[i].setOptions({
				fillColor: color,
				fillOpacity: 0.9
			});
		}
		else if(rect_speed == 0){
			rectArr[i].setOptions({
				fillColor: "#000000",  //any color will do as long as transparent
				fillOpacity: 0.0
			});
		}
	}
}

function RPsetMap(map) {
	for (var i = 0; i < rp_markers.length; i++) {
	  rp_markers[i].setMap(map);
	}
}
function RPC1setMap(map) {
	for (var i = 0; i < rpc1_markers.length; i++) {
	  rpc1_markers[i].setMap(map);
	}
}
function RPC2setMap(map) {
	for (var i = 0; i < rpc2_markers.length; i++) {
	  rpc2_markers[i].setMap(map);
	}
}
function WsetMap(map) {
	for (var i = 0; i < w_markers.length; i++) {
	  w_markers[i].setMap(map);
	}
}
function WSsetMap(map) {
	for (var i = 0; i < ws_markers.length; i++) {
	  ws_markers[i].setMap(map);
	}
}

function redrawRectangle(map){
	for (var i = 0; i < rectArr.length; i++) {
		rectArr[i].setMap(map);
	}
}

function toggleRP() {
	if(document.getElementById("rp_button").classList.contains("active")){
		document.getElementById("rp_button").classList.remove("active");
		document.getElementById("rp_button").classList.add("inactive");
		RPsetMap(null);
	}
	else if(document.getElementById("rp_button").classList.contains("inactive")){
		document.getElementById("rp_button").classList.remove("inactive");
		document.getElementById("rp_button").classList.add("active");
		RPsetMap(map);
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
	
	redrawRectangle(null);
	countRectAP();
	redrawRectangle(map);
	document.getElementById("grid_legend_table_time").style.display = "none";
	document.getElementById("grid_legend_table_speed").style.display = "none";
	document.getElementById("grid_legend_table_ap").style.display = "block";
}
function toggleRPC1() {
	if(document.getElementById("rpc1_button").classList.contains("active")){
		document.getElementById("rpc1_button").classList.remove("active");
		document.getElementById("rpc1_button").classList.add("inactive");
		RPC1setMap(null);
	}
	else if(document.getElementById("rpc1_button").classList.contains("inactive")){
		document.getElementById("rpc1_button").classList.remove("inactive");
		document.getElementById("rpc1_button").classList.add("active");
		RPC1setMap(map);
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
	
	redrawRectangle(null);
	countRectAP();
	redrawRectangle(map);
	document.getElementById("grid_legend_table_time").style.display = "none";
	document.getElementById("grid_legend_table_speed").style.display = "none";
	document.getElementById("grid_legend_table_ap").style.display = "block";
}
function toggleRPC2() {
	if(document.getElementById("rpc2_button").classList.contains("active")){
		document.getElementById("rpc2_button").classList.remove("active");
		document.getElementById("rpc2_button").classList.add("inactive");
		RPC2setMap(null);
	}
	else if(document.getElementById("rpc2_button").classList.contains("inactive")){
		document.getElementById("rpc2_button").classList.remove("inactive");
		document.getElementById("rpc2_button").classList.add("active");
		RPC2setMap(map);
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
	
	redrawRectangle(null);
	countRectAP();
	redrawRectangle(map);
	document.getElementById("grid_legend_table_time").style.display = "none";
	document.getElementById("grid_legend_table_speed").style.display = "none";
	document.getElementById("grid_legend_table_ap").style.display = "block";
}
function toggleW() {
	if(document.getElementById("w_button").classList.contains("active")){
		document.getElementById("w_button").classList.remove("active");
		document.getElementById("w_button").classList.add("inactive");
		WsetMap(null);
	}
	else if(document.getElementById("w_button").classList.contains("inactive")){
		document.getElementById("w_button").classList.remove("inactive");
		document.getElementById("w_button").classList.add("active");
		WsetMap(map);
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
	
	redrawRectangle(null);
	countRectAP();
	redrawRectangle(map);
	document.getElementById("grid_legend_table_time").style.display = "none";
	document.getElementById("grid_legend_table_speed").style.display = "none";
	document.getElementById("grid_legend_table_ap").style.display = "block";
}

function toggleWS() {
	if(document.getElementById("ws_button").classList.contains("active")){
		document.getElementById("ws_button").classList.remove("active");
		document.getElementById("ws_button").classList.add("inactive");
		WSsetMap(null);
	}
	else if(document.getElementById("ws_button").classList.contains("inactive")){
		document.getElementById("ws_button").classList.remove("inactive");
		document.getElementById("ws_button").classList.add("active");
		WSsetMap(map);
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
	
	redrawRectangle(null);
	countRectAP();
	redrawRectangle(map);
	document.getElementById("grid_legend_table_time").style.display = "none";
	document.getElementById("grid_legend_table_speed").style.display = "none";
	document.getElementById("grid_legend_table_ap").style.display = "block";
}

function toggleTime(){
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
		redrawRectangle(null);
		countRectAP();
		redrawRectangle(map);
		document.getElementById("grid_legend_table_time").style.display = "none";
		document.getElementById("grid_legend_table_speed").style.display = "none";
		document.getElementById("grid_legend_table_ap").style.display = "block";
	}
	else if(document.getElementById("time_button").classList.contains("inactive")){
		document.getElementById("time_button").classList.remove("inactive");
		document.getElementById("time_button").classList.add("active");
		redrawRectangle(null);
		countRectTime();
		redrawRectangle(map);
		document.getElementById("grid_legend_table_time").style.display = "block";
		document.getElementById("grid_legend_table_speed").style.display = "none";
		document.getElementById("grid_legend_table_ap").style.display = "none";
	}
	
	//set Speed button to inactive if it is active
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
	}
}

function toggleSpeed(){
	if(document.getElementById("speed_button").classList.contains("active")){
		document.getElementById("speed_button").classList.remove("active");
		document.getElementById("speed_button").classList.add("inactive");
		redrawRectangle(null);
		countRectAP();
		redrawRectangle(map);
		document.getElementById("grid_legend_table_time").style.display = "none";
		document.getElementById("grid_legend_table_speed").style.display = "none";
		document.getElementById("grid_legend_table_ap").style.display = "block";
		
	}
	else if(document.getElementById("speed_button").classList.contains("inactive")){
		document.getElementById("speed_button").classList.remove("inactive");
		document.getElementById("speed_button").classList.add("active");
		redrawRectangle(null);
		countRectSpeed();
		redrawRectangle(map);
		document.getElementById("grid_legend_table_time").style.display = "none";
		document.getElementById("grid_legend_table_speed").style.display = "block";
		document.getElementById("grid_legend_table_ap").style.display = "none";
	}
	
	//set Time Spent button to inactive if it is active
	if(document.getElementById("time_button").classList.contains("active")){
		document.getElementById("time_button").classList.remove("active");
		document.getElementById("time_button").classList.add("inactive");
	}
}

function getWDBtxt(){
	var filter_count = 0;
	var filtered_ws_macs = [];
	for(i = 0; i < rectArr.length; i++){
		//only check those rectangle with gps readings
		if(has_readings[i] == 1){
			for(x = 0; x < ws_lat.length; x++){
				var point = new google.maps.LatLng(ws_lat[x], ws_lng[x]);
				if(rectArr[i].getBounds().contains(point)){
					filter_count++;
					filtered_ws_macs.push(ws_macs[x]);
				}
			}
		}
	}
	for(i=0; i< filtered_ws_macs.length; i++){
		console.log(filtered_ws_macs[i]);
	}
}

function LatCoordDistance(lat,offset){
	var R = 6378137;

	//convert the offset
	rad_lat_offset = offset/R;
	
	//new coordinates, to degrees
	new_lat = (lat - rad_lat_offset * 180/Math.PI).toFixed(6);
	
	//console.log(parseFloat(new_lat));
	return parseFloat(new_lat);
}

function LngCoordDistance(lat,lng,offset){
	var R = 6378137;

	//convert the offset
	rad_lng_offset =  offset/(R*Math.cos(Math.PI/180*lat));
	
	//new coordinates, to degrees
	new_lng = (lng + rad_lng_offset * 180/Math.PI).toFixed(6);

	//console.log(parseFloat(new_lng));
	return parseFloat(new_lng);
}

function downloadUrl(url, callback) {
	var request = window.ActiveXObject ?
		new ActiveXObject('Microsoft.XMLHTTP') :
		new XMLHttpRequest;

	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			request.onreadystatechange = doNothing;
			callback(request, request.status);
		}
	};

	request.open('GET', url, true);
	request.send(null);
}

function doNothing() {}
</script>
    <script
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz_xDT4_D32UQ__xr91UT-_P9a7bcOG2Q&callback=gridMap&libraries=geometry">
    </script>
  </body>
</html>