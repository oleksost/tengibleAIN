/*
EVENTS
1 - installation of  a new aset
2 - new asset installed, show new asset information
3 - Asset is brocken
4 - new update service Bulletin
5 - Asset repaired
6 - asset can be pimped 
7 - Asset is pimped
*/

var initial_asset = "a0";
var initial_marketing = "event0";
var initial_instruction = "event0";
//var initial_url = "http://veui5infra.dhcp.wdf.sap.corp:8080/sapui5-sdk-dist/explored.html#/sample/sap.uxap.sample.AlternativeProfileObjectPageHeader/preview";




// Replace Text of Marketing
function replace_marketing(event_){
	$( "#marketing_headline" ).text(marketing[event_][0]);
	$( "#marketing_text" ).text(marketing[event_][1]);
}

// Replace Text of Digital Twin
function replace_asset(asset_){
    console.log(asset_);
	$( "#twin_id" ).text(asset[asset_][0]);
	$( "#twin_model" ).text(asset[asset_][1]);
	$( "#twin_status" ).text(asset[asset_][2]);
	if (!(asset_=="a000")){
	$( "#asset_image" ).attr('src', "static/img/"+asset[asset_][3]+".gif"); 
	}else {$( "#asset_image" ).attr('src', "");}
}


// Replace the Instructions and the speaker
function replace_instruction(event_){
	$( "#container_speach").text(instruction[event_][0]);
	//replace the speaker
	console.log(instruction[event_][1][0]);
	$( "#speaker" ).text(instruction[event_][1][0]);
	//replace the speaker's image
	$( "#container_minifigure" ).css('background-image', "url(static/img/"+instruction[event_][1][1]);
	
}

// Replace Source of iFrame
function replace_iframe(current_url){
	$("#ain").attr('src', current_url); 
}



// Reset all Values, event number and rfid number of the asset as input variables
function reset_all_texts(event_nr, esset_rfid_id){
    var event_="event"+event_nr.toString();
	replace_marketing(event_);
	replace_instruction(event_);
	if(!(esset_rfid_id==0) && !(event_nr==1) ){
	
	    var asset = "a"+esset_rfid_id.toString();
	    replace_asset(asset);    
	}else if (event_nr==1 || event_nr==0){
	//is no asset on the rfid
	    var asset_ = "a"+"000";
	    replace_asset(asset_);
	}
	//replace_iframe(initial_url);
	console.log("all texts reset");
}
    

//STOP DEMO
function stop_demo(){
        $.ajax({
            type: 'GET',
            url: "/stop/",
            data: 0,
            success: function (data) {
              
             }
        });
}

// INITIAL SETUP
$( document ).ready(function() {
	console.log("document loaded");
	//test
	//reset_all_texts(0, 0);
	if ("WebSocket" in window){
           //var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           var messagecount = 0
           ws.onmessage = function(evt) {
              messagecount += 1;
              //jQuery(".hold").attr('id','pieSlice' + evt.data);
              var event = JSON.parse(evt.data);
              event_nr=event.event;
              esset_rfid_id=event.asset_rfid_id;
              reset_all_texts(event_nr, esset_rfid_id);
              //alert("Hallo");
              //jQuery("#container_speach").html(evt.data);
           }
           ws.onopen = function() {
              messagecount = 0;
           }
           ws.onclose = function() {
              messagecount = 0;
           }
        }
        else {
           alert("WebSocket NOT support by your Browser!");
        }
});

//START THE DEMO
$("#button_start").click(function(evt) {
    console.log("starting...");
     $.ajax({
            type: 'GET',
            url: "/start/",
            success: function (data) {            
               $('#button_start').off('click');
               $('#button_start').on('click.mynamespace', function() { alert("Alrteady running")});
            }
        });
     });

$("#button_stop").click(function(evt) {
     $.ajax({
            type: 'GET',
            url: "/stop/",
            success: function (data) {
               $('#button_start').off('click');
               $('#button_start').on('click.mynamespace', function() { 
                $.ajax({
            type: 'GET',
            url: "/start/",
            data: 1,
            success: function (data) {            
               $('#button_start').off('click');
               $('#button_start').on('click.mynamespace', function() { alert("Alrteady running")});
            }
        });
               });
             }
        });
     });
     
//STOP EXECUTION ON RELOAD 
window.onbeforeunload = function(event){ 
           stop_demo();
    };     


