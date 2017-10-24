<!DOCTYPE html >
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <title>Using MySQL and PHP with Google Maps</title>
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
    </style>
  </head>

  <body>
    <div id="map"></div>

    <script>
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
      }
	  
function gridMap() { 
	var map = new google.maps.Map(document.getElementById('map'), 
		{ 
			zoom: 18, 
			center: {lat: 14.676208, lng: 121.043861},
			mapTypeId: 'terrain' 
		}
	);
	//initialize infoWindow
	var infoWindow = new google.maps.InfoWindow;
	//these arrays will be used to determine if an access point is inside a grid
	var latitudes = [];
	var longitudes = [];

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
				parseFloat(ap.getAttribute('lng'))
			);
			latitudes.push(parseFloat(ap.getAttribute('lat')));
			longitudes.push(parseFloat(ap.getAttribute('lng')));
		
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
				label: id,
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
		/*
		//test rectangles for plotting grids manually
		var rectangle = new google.maps.Rectangle({ 
			strokeColor: '#000000', 
			strokeOpacity: 0.5, 
			strokeWeight: 1, 
			fillColor: '#000000', 
			fillOpacity: 0.0, 
			map: map, 
			bounds: { 
				north: 14.676208, 
				south: 14.677008, 
				east: 121.038961, 
				west: 121.038161 
			} 
		});
		var rectangle2 = new google.maps.Rectangle({ 
			strokeColor: '#000000', 
			strokeOpacity: 0.5, 
			strokeWeight: 1, 
			fillColor: '#000000', 
			fillOpacity: 0.0, 
			map: map, 
			bounds: { 
				north: 14.676208, 
				south: 14.677008, 
				east: 121.039761, 
				west: 121.038961 
			} 
		});
		var rectangle3 = new google.maps.Rectangle({ 
			strokeColor: '#000000', 
			strokeOpacity: 0.5, 
			strokeWeight: 1, 
			fillColor: '#000000', 
			fillOpacity: 0.0, 
			map: map, 
			bounds: { 
				north: 14.676208, 
				south: 14.677008, 
				east: 121.040561, 
				west: 121.039761  
			} 
		});
		var rectangle4 = new google.maps.Rectangle({ 
			strokeColor: '#000000', 
			strokeOpacity: 0.5, 
			strokeWeight: 1, 
			fillColor: '#000000', 
			fillOpacity: 0.0,  
			map: map, 
			bounds: { 
				north: 14.676208, 
				south: 14.677008, 
				east: 121.041361, 
				west: 121.040561  
			} 
		});*/
		/*var point = new google.maps.LatLng(14.676308,121.043861);
		var marker = new google.maps.Marker({
		map: map,
		position: point,
		label: "AP",
		});*/
		
		//initial bounds
		var north = 14.676208;
		var south = 14.677008;
		var east = 121.040561;
		var west = 121.039761;
		var rectangle,count;
		for(j=0; j < 5; j++){
			if(j==0){
				//
			}
			else{
				north = south;
				south = +((north - 0.000800).toFixed(6));
				east = 121.040561;
				west = 121.039761;
			}
			for(i=0; i < 10; i++){
				if(i==0){
					/*console.log(i+"------------");
					console.log("NORTH: "+north);
					console.log("SOUTH: "+south);
					console.log("EAST: "+east);
					console.log("WEST: "+west);*/
				}
				else{
					west = east;
					east = +((west + 0.000800).toFixed(6));
					/*console.log(i+"------------");
					console.log("NORTH: "+north);
					console.log("SOUTH: "+south);
					console.log("EAST: "+east);
					console.log("WEST: "+west);*/
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
				/*
				//test if a point can be located in a grid
				if(rectangle.getBounds().contains(point)){
					console.log("DIM: "+ j +"th row x "+ i +"th column");
				}*/
				
				//loop through our points and check whether it is inside this grid/rectangle being drawn
				count = 0;
				for(x = 0; x < latitudes.length; x++){
					/*
					//print elements latitudes and longitudes array
					console.log("Lat "+ x + ": " + latitudes[x]);
					console.log("Long "+ x + ": " + longitudes[x]);*/
					var point = new google.maps.LatLng(latitudes[x], longitudes[x]);
					if(rectangle.getBounds().contains(point)){
						count++;
					}
				}
				if(count >= 10){
					//change the color of this rectangle to red
					rectangle.setOptions({
						fillColor: "#FF493F",
						fillOpacity: 0.5
					});
				}
				else if(count >= 5){
					//change the color of this rectangle to yellow
					rectangle.setOptions({
						fillColor: "#FFF200",
						fillOpacity: 0.5
					});
				}
				else if(count > 0 && count < 5){
					//change the color of this rectangle to green
					rectangle.setOptions({
						fillColor: "#4DFF3D",
						fillOpacity: 0.5
					});
				}
			}
		}
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
}

function doNothing() {}
</script>
    <script
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz_xDT4_D32UQ__xr91UT-_P9a7bcOG2Q&callback=gridMap">
    </script>
  </body>
</html>