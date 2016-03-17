/*
EVENTS
1 - installation of  a new aset
2 - new asset installed, show new asset information
3 - Asset is brocken
4 - new update service Bulletin
5 - Asset repaired
6 - asset can be pimped 
7 - Asset is pimped
8 - display a new hint
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
	//$( "#twin_status" ).text(asset[asset_][2]);
	if (!(asset_=="a000")){
	$( "#asset_image" ).attr('src', "static/img/"+asset[asset_][2]);  
	}else 
	   {
       //TODO: IMAGE FOR THE EVENT 000
           $( "#asset_image" ).attr('src', "");
       }
}

//updating the asset status
function update_asset_status(event){
switch (event){
       case 3:  
              $( "#twin_status" ).text("broken");
              break;
       case 2:  
              $( "#twin_status" ).text("working");
              break;  
       case 5:  
              $( "#twin_status" ).text("working");
              break; 
              
    }
    
       
}

// Replace the Instructions and the speaker
function replace_instruction(event_){
	$( "#container_speach").text(instruction[event_][0]);
	//replace the speaker
	console.log(instruction[event_][1]);
	$( "#speaker" ).text(instruction[event_][1][0]);
	//replace the speaker's image
	$( "#container_minifigure" ).css('background-image', "url(static/img/"+instruction[event_][1][1]);
	
}

// Replace Source of iFrame
function replace_iframe(current_url){
	$("#ain").attr('src', current_url); 
}

function display_hint(fint_nr){
  var hint = "h"+fint_nr.toString();
  $( "#hints" ).text(hints[hint][0]); 
  //console.log(hints[hint][0]);
}


// Reset all Values, event number and rfid number of the asset as input variables
function reset_all_texts(event_nr, esset_rfid_id, fint_nr){
//event 8 does not change any instructions/marketing or speaker
if (!(event_nr==8)){
    var event_="event"+event_nr.toString();
	replace_marketing(event_);
	replace_instruction(event_);
	update_asset_status(event_nr);
	//
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
	}else{
	//display hints for event 8
	if (fint_nr>0){
	   display_hint(fint_nr);
	}	
	}
}
    

//STOP DEMO
function stop_demo(){
        $.ajax({
            type: 'GET',
            url: "/stop/",
            data: 0,
            async: false,
            success: function (data) {
              
             }
        });
}
function start_demo(){
console.log("starting...");
     $.ajax({
            type: 'GET',
            url: "/start/",
            success: function (data) {            
              
            }
        });
}

// INITIAL SETUP
$( document ).ready(function() {
	console.log("document loaded");
	//test
	reset_all_texts(0, 0);
	
	if ("WebSocket" in window){
           var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           //var ws = new WebSocket("ws://0.0.0.0:5000/websocket"); 
           var messagecount = 0;
           start_demo();
           ws.onmessage = function(evt) {
              
              messagecount += 1;
              //jQuery(".hold").attr('id','pieSlice' + evt.data);
              var event = JSON.parse(evt.data);
              event_nr=event.event;
              esset_rfid_id=event.asset_rfid_id;
              hint_nr=event.hint;
              reset_all_texts(event_nr, esset_rfid_id,hint_nr);
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
/*$("#button_start").click(function(evt) {
    console.log("starting...");
     $.ajax({
            type: 'GET',
            url: "/start/",
            success: function (data) {            
               $('#button_start').off('click');
               $('#button_start').on('click.mynamespace', function() { alert("Alrteady running")});
            }
        });
     });*/
/*
$("#button_stop").click(function(evt) {
  console.log("reloading");
  location.reload();
     });
   */  
//STOP EXECUTION ON RELOAD 
window.onbeforeunload = function(event){ 
           stop_demo();
    };     


