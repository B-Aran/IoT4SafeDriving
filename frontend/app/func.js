//Centro del mapa a cambiar
const lat_lega = 40.330;
const lng_lega = -3.765;

//Variables del mapa
let map;
var polylines = [];
var markers = [];
var export_value = false;

const api_url = "http://127.0.0.1:5000/datos";
const get_url = "http://127.0.0.1:5000/charge";

function initMap() {
    //set up the map
    var mapDiv = document.getElementById("map");
    var myOptions = {
      zoom: 17,
      center: new google.maps.LatLng(lat_lega, lng_lega),
      mapTypeControl: true,
      mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
       }
    }
    var map = new google.maps.Map(mapDiv, myOptions);

    //Create DropDownMenu for selecting vehicles
    //create the options that respond to click
    var divOptions = {
            gmap: map,
            name: 'All vehicles',
            title: "This acts like a button or click event",
            id: "mapOpt",
            action: function(){
                alert('option1');
            }
    }
    var optionDiv1 = new optionDiv(divOptions);

    var divOptions2 = {
            gmap: map,
            name: 'Option2',
            title: "This acts like a button or click event",
            id: "satelliteOpt",
            action: function(){
                alert('option2');
            }
    }

    var optionDiv2 = new optionDiv(divOptions2);

    //create the check box items
    var checkOptions = {
            gmap: map,
            title: "This allows for multiple selection/toggling on/off",
            id: "terrainCheck",
            label: "On/Off",
            action: function(){
                alert('you clicked check 1');
            }
    }
    var check1 = new checkBox(checkOptions);

    var checkOptions2 = {
            gmap: map,
            title: "This allows for multiple selection/toggling on/off",
            id: "myCheck",
            label: "my On/Off",
            action: function(){
                alert('you clicked check 2');
            }
    }
    var check2 = new checkBox(checkOptions2);

    //create the input box items

    //possibly add a separator between controls
    var sep = new separator();

    //put them all together to create the drop down
    var ddDivOptions = {
        items: [optionDiv1, optionDiv2, sep, check1, check2],
        id: "myddOptsDiv"
    }
    //alert(ddDivOptions.items[1]);
    var dropDownDiv = new dropDownOptionsDiv(ddDivOptions);

    var dropDownOptions = {
            gmap: map,
            name: 'Select Vehicules',
            id: 'ddControl',
            title: 'A custom drop down select with mixed elements',
            position: google.maps.ControlPosition.TOP_RIGHT,
            dropDown: dropDownDiv
    }

    var dropDown1 = new dropDownControl(dropDownOptions);
    paint_data(map);
}
function change_export_value(){
    if(export_value){
        export_value = false;
    }
    else export_value = true;
}
function getFormattedTime(time){
    let unix_timestamp = time;
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds.
    var date = new Date(unix_timestamp * 1000);
    // Hours part from the timestamp
    var hours = date.getHours();
    // Minutes part from the timestamp
    var minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    var seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    var formattedTime = hours + ' H ' + minutes.substr(-2) + ' M ' + seconds.substr(-2) + ' S';

    return formattedTime
}

async function get_points(){
    fetch(get_url).then(function(response){
        return response.json();
    }).then(function(data){
        console.log(data)
        return data;
    })
}

async function paint_data(map){
    var response = await fetch(get_url);
    var data = await response.json();
    var line = [];
    for (let i in data){
        aux = {lat: parseFloat(data[i]["geometry"]["coordinates"][1]) , lng: parseFloat(data[i]["geometry"]["coordinates"][0])};
        //Prepare for polyline
        line.push(aux)
        //Add new marker
        text = "Lat: " + data[i]["geometry"]["coordinates"][1]+ " Lon: "+ data[i]["geometry"]["coordinates"][0] + " Yaw: "+data[i]["properties"]["yaw"];
        const infoWindow = new google.maps.InfoWindow({content: text,});
        const popup = new google.maps.InfoWindow({content: text,});
        const marker = new google.maps.Marker({position: aux, map, title: "Point "+i,icon:{path:google.maps.SymbolPath.CIRCLE, scale:3,},});
        marker.addListener("click", () => {infoWindow.open({anchor: marker,map,shouldFocus: false,});});
        markers.push(marker);
    }

    //Paint polyline
    const polyline = new google.maps.Polyline({
        path: line,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
      });
     polyline.setMap(map);
     polylines.push(polyline)
}

async function get_interval(){
    //Cogemos valores en un intervalo de tiempo
    var fecha_ini = document.getElementById("ini").value;
    var fecha_fin = document.getElementById("fin").value;
    const ini = +new Date(fecha_ini)
    const fin = +new Date(fecha_fin)
    //Call the API
    var interval_url = "http://127.0.0.1:5000/get_interval?fecha_ini="+ini+"&fecha_fin="+fin;
    const response = await fetch(interval_url)
    const data = await response.json()
    //If we want to export to csv
    if(export_value){
        //JSON to CSV
        var json = data;
        var fields = Object.keys(json[0])
        var replacer = function(key, value) { return value === null ? '' : value }
        var csv = json.map(function(row){
          return fields.map(function(fieldName){
            return JSON.stringify(row[fieldName], replacer)
          }).join(',')
        })
        csv.unshift(fields.join(',')) // add header column
         csv = csv.join('\r\n');
        //Select the filename and download the file
        var filename = "Data_"+ini+"_"+fin+".csv";
        var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        if (navigator.msSaveBlob) { // IE 10+
            navigator.msSaveBlob(blob, filename);
        } else {
            var link = document.createElement("a");
            if (link.download !== undefined) { // feature detection
                // Browsers that support HTML5 download attribute
                var url = URL.createObjectURL(blob);
                link.setAttribute("href", url);
                link.setAttribute("download", filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }
    }
    //Borramos markers y polylines antiguas
    for (let i in markers){
        markers[i].setMap(null);
    }
    markers = [];
    for(let i in polylines){
        polylines[i].setMap(null);
    }
    polylines = [];

    //Pintamos nueva polyline y markers y añadimos a arrays globales.
    line = [];
    for (let i in data){
        aux = {lat: parseFloat(data[i]["geometry"]["coordinates"][1]) , lng: parseFloat(data[i]["geometry"]["coordinates"][0])};
        //Prepare for polyline
        line.push(aux)
        //Add new marker
        text = "Lat: " + data[i]["geometry"]["coordinates"][1]+ " Lon: "+ data[i]["geometry"]["coordinates"][0] + " Yaw: "+data[i]["properties"]["yaw"];
        const infoWindow = new google.maps.InfoWindow({content: text,});
        const popup = new google.maps.InfoWindow({content: text,});
        const marker = new google.maps.Marker({position: aux, map, title: "Point "+i,icon:{path:google.maps.SymbolPath.CIRCLE, scale:3,},});
        marker.addListener("click", () => {infoWindow.open({anchor: marker,map,shouldFocus: false,});});
        markers.push(marker);
    }

    //Paint polyline
    const polyline = new google.maps.Polyline({
        path: line,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
      });
     polyline.setMap(map);
     polylines.push(polyline)
}


example = get_points();
console.log(example);
initMap();
