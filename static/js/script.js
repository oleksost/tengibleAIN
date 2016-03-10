

var initial_asset = "a1";
var initial_marketing = "m1";
var initial_instruction = "i1";
var initial_url = "http://veui5infra.dhcp.wdf.sap.corp:8080/sapui5-sdk-dist/explored.html#/sample/sap.uxap.sample.AlternativeProfileObjectPageHeader/preview";




// Replace Text of Marketing
function replace_marketing(current_marketing){
	$( "#marketing_headline" ).text(marketing[current_marketing][0]);
	$( "#marketing_text" ).text(marketing[current_marketing][1]);
}

// Replace Text of Digital Twin
function replace_asset(current_asset){
	$( "#twin_id" ).text(asset[current_asset][0]);
	$( "#twin_model" ).text(asset[current_asset][1]);
	$( "#twin_status" ).text(asset[current_asset][2]);
	$( "#asset_image" ).attr('src', "static/img/"+asset[current_asset][3]+".gif"); 
}


// Replace the Text of the Instructions
function replace_instruction(current_instruction){
	$( "#container_speach").text(instruction[current_instruction][0]);
}


// Replace Source of iFrame
function replace_iframe(current_url){
	$("#ain").attr('src', current_url); 
}



// Reset all Values, event number and rfid number of the asset as input variables
function reset_all_texts(event_nr, esset_rfid_id){
	replace_marketing(initial_marketing);
	replace_asset(initial_asset);
	replace_instruction(initial_instruction);
	//replace_iframe(initial_url);
	console.log("all texts reset");
}

// TRY TO CALL THIS FUNCTION VIA THE RASPBERRY PI
function python_test(){
	console.log("python test successfull");
	replace_marketing("m2");
	replace_asset("a3");
	//replace_instruction("i1");
	replace_iframe("http://www.w3schools.com/");
}

//STOP 
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
	if ("WebSocket" in window){
           var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           var messagecount = 0
           ws.onmessage = function(evt) {
              messagecount += 1;
              //jQuery(".hold").attr('id','pieSlice' + evt.data);
              var event = JSON.parse(evt.data);
              event_nr=event.event;
              esset_rfid_id=event.asset_rfid_id;
              //reset_all_texts(event_nr, esset_rfid_id);
              jQuery("#container_speach").html(evt.data);
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

