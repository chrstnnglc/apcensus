<!DOCTYPE html >
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <title>Using MySQL and PHP with Google Maps</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 80%;
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
		border-top: 3px solid black;
		border-bottom: 3px solid black;
		padding: 25px 0 25px 0;
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
	  #w_button{
		background-color: rgb(58,111,237);
	  }
    </style>
  </head>

  <body>
    <div id="map"></div>
	<div id="selection_buttons">
		<input onclick="toggleWS()" type="button" value="Wigle Site" id="ws_button" class="buttons active">
		<input onclick="toggleRP()" type="button" value="RasPi" id="rp_button" class="buttons active">
		<input onclick="toggleW()" type="button" value="Wigle" id="w_button" class="buttons active">
	</div>

<script>
var ws_markers = [];
var rp_markers = [];
var w_markers = [];
var rectArr = [];
var ws_lat = [];
var ws_lng = [];
var rp_lat = [];
var rp_lng = [];
var w_lat = [];
var w_lng = [];
var rpCountArr = [];
var wCountArr = [];
var wsCountArr = [];
var rectCountArr = [];
var map, rp_count, w_count, ws_count, rect_count, total_count;
function gridMap() { 
	map = new google.maps.Map(document.getElementById('map'), 
		{ 
			zoom: 19, 
			center: {lat: 14.659672, lng: 121.067834},
			mapTypeId: 'terrain' 
		}
	);
	//initialize infoWindow
	var infoWindow = new google.maps.InfoWindow;
	var macs = [];

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
			else if (label == "wigle"){
				w_lat.push(parseFloat(ap.getAttribute('lat')));
				w_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			else if (label == "wiglesite"){
				ws_lat.push(parseFloat(ap.getAttribute('lat')));
				ws_lng.push(parseFloat(ap.getAttribute('lng')));
			}
			macs.push(mac);
			
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
			else if (label == "wigle"){
				icon = 'w_marker.png'
			}
			else if (label == "wiglesite"){
				icon = 'ws_marker.png'
			}
			var marker = new google.maps.Marker({
				map: map,
				position: point,
				icon: icon
			});
			//assign corresponding markers to array
			if (label == "rpi"){
				rp_markers.push(marker)
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
		
		//initial bounds
		var north = 14.660184;
		var south = 14.660031;
		var east = 121.067174;
		var west = 121.067021;
		var rectangle;
		total_count = 0;
		for(j=0; j < 7; j++){
			if(j==0){
				//do nothing
			}
			else{
				north = south;
				south = +((north - 0.000153).toFixed(6));
				east = 121.067174;	//set the value of this equal to the initial east bound
				west = 121.067021;	//set the value of this equal to the initial west bound
			}
			for(i=0; i < 10; i++){
				if(i==0){
					//do nothing
				}
				else{
					west = east;
					east = +((west + 0.000153).toFixed(6));
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
				w_count = 0;
				ws_count = 0;
				rect_count = 0;
				for(x = 0; x < rp_lat.length; x++){
					var point = new google.maps.LatLng(rp_lat[x], rp_lng[x]);
					if(rectangle.getBounds().contains(point)){
						rp_count++;
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
				rect_count = rp_count + w_count + ws_count;
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
				wCountArr.push(w_count);
				wsCountArr.push(ws_count);
				rectCountArr.push(String(rect_count));
				total_count = total_count + rect_count
			}
		}
		console.log("Total Count: " + total_count)
		
		//add event listners for each rectangle and get the count in that rectangle
		for(i = 0; i < rectArr.length; i++){
			google.maps.event.addListener(rectArr[i],'click', function(event) {
				for(j = 0; j < rectArr.length; j++){
					if(rectArr[j].getBounds().contains(event.latLng)){
						rect_count = rectCountArr[j];
					}
				}
				infoWindow.setContent("# of APs: <b>" + String(rect_count) + '</b>')
				infoWindow.setPosition(event.latLng);
				infoWindow.open(map);
			}); 
		}
	});
}

function countRect(){
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
			rectArr[i].setOptions({
				fillColor: color,
				fillOpacity: 0.9
			});
		}
		if (rect_count == 0){
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

function RPsetMap(map) {
	for (var i = 0; i < rp_markers.length; i++) {
	  rp_markers[i].setMap(map);
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
	redrawRectangle(null);
	countRect();
	redrawRectangle(map);
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
	redrawRectangle(null);
	countRect();
	redrawRectangle(map);
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
	redrawRectangle(null);
	countRect();
	redrawRectangle(map);
}
	
	/*
		//initialize map centered at Quezon City
        function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(14.676208,121.043861),
          zoom: 18
        });
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
              var isp = ap.getAttribute('isp');
              var point = new google.maps.LatLng(
                  parseFloat(ap.getAttribute('lat')),
                  parseFloat(ap.getAttribute('lng')));
			  
			  //set the content of the infoWindow
              var infowincontent = document.createElement('div');
              var strong = document.createElement('strong');
              strong.textContent = ssid
              infowincontent.appendChild(strong);
              infowincontent.appendChild(document.createElement('br'));
			  
			  mac = "MAC: " + mac;
			  isp = "ISP: " + isp;
              var text = document.createElement('text');
              text.textContent = mac
              infowincontent.appendChild(text);
			  infowincontent.appendChild(document.createElement('br'));
			  var text = document.createElement('text');
              text.textContent = isp
              infowincontent.appendChild(text);
			  
			  //plot the marker in the map
              var marker = new google.maps.Marker({
                map: map,
                position: point,
                label: "AP",
              });
			  
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
          });
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
      }*/

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
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz_xDT4_D32UQ__xr91UT-_P9a7bcOG2Q&callback=gridMap">
    </script>
  </body>
</html>