/*
EVENTS
1 - installation of  a new aset
2 - new asset installed, show new asset information
  2.e0 - asset registration
  2.e1 - asset synchronisation
  2.e2 - asset synchronisation Manufacturer responce
3 - Asset is brocken
4 - new update service Bulletin
5 - Asset repaired
6 - asset can be pimped 
7 - Asset is pimped
8 - display a new hint
*/

var paused=false;
var timeout;
var timeout_e1=null;
var installed=true;
var current_asset;
var current_event;
var last_image="";
var current_speaker;
var last_animation_ready=true;
var cerrent_instruction="screenshot1";
var event_backup = [];

function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}


//var initial_asset = "a0";
//var initial_marketing = "event0";
//var initial_instruction = "event0";
//var initial_url = "http://veui5infra.dhcp.wdf.sap.corp:8080/sapui5-sdk-dist/explored.html#/sample/sap.uxap.sample.AlternativeProfileObjectPageHeader/preview";

// Switch between iFrame and screenshots
function screen_mode(mode){
  console.log("changing screenmode to "+mode);
 $("#container_iframe").empty(); // clears iframe container
 switch(mode){
    case "screenshot":  $("#container_iframe").append("<img id='screenshot' src='static/img/screenshot1.jpg' alt='Screenshot missing'>");
                        console.log("changed to screenshot");
          break;
    case "iframe": $("#container_iframe").append("<iframe id='ain' src='http://veui5infra.dhcp.wdf.sap.corp:8080/sapui5-sdk-dist/explored.html#/sample/sap.uxap.sample.AlternativeProfileObjectPageHeader/preview'></iframe>");
          console.log("changed to iframe");
          break;
    default: $("#container_iframe").append("<img id='screenshot' src='static/img/screenshot1.jpg' alt='Screenshot missing'>");   
            console.log("changed to default");

  }
}



// Replace Text of Marketing
function replace_marketing(event_,subevent){
// fade out


  $( "#marketing_text" ).animate({
    opacity: 0,
  }, 500, function() {
  // Animation complete
  
    if (event_=="event2"){
     $( "#marketing_headline" ).text(marketing[event_][subevent][0]);
     $( "#marketing_text" ).text(marketing[event_][subevent][1]);
    
    }else{
	$( "#marketing_headline" ).text(marketing[event_][0]);
	$( "#marketing_text" ).text(marketing[event_][1]);
    }
  
    // fade in
 $( "#marketing_text" ).animate({
    opacity: 1,
  }, 500);
  
  });
}

// Replace Text of Digital Twin
function replace_asset(asset_, pimped){
    console.log(asset_);
	$( "#twin_id" ).text(asset[asset_][0]);
	$( "#twin_model" ).text(asset[asset_][1]);
	if (pimped==true){
	  $( "#asset_image" ).attr('src', asset[asset_][3]);
	  $( "#twin_id" ).text(asset[asset_][4]);
	}else{
	  $( "#asset_image" ).attr('src', asset[asset_][2]);
	  $( "#twin_id" ).text(asset[asset_][0]);
	  
	}
}

function replace_asset_boosted(asset_){

$( "#asset_image" ).attr('src', asset[asset_][3]);


}

//updating the asset status
function update_asset_status(event){
switch (event){
       case 3:  
              $( "#twin_status" ).text("broken");
              //console.log("setting class "+" error");
              $( "#twin_status" ).css("color","#f94865");
              //$( "#twin_status" ).toggleClass("error");
              break;
       case 5:
              $( "#twin_status" ).text("working");
              $( "#twin_status" ).css("color","#44ef69");
              //console.log("setting class "+" working");
              //$( "#twin_status" ).toggleClass("working");
              break;   
       case 2:  
              $( "#twin_status" ).text("working");
              $( "#twin_status" ).css("color","#44ef69");
              //console.log("setting class "+" working");
              //$( "#twin_status" ).toggleClass("working");
              break;  
       case 1: 
              $( "#twin_status" ).text("...");
              $( "#twin_status" ).css("color","#fff");
              //console.log("setting class "+" neutral");
              //$( "#twin_status" ).toggleClass("neutral");
              break; 
       case 0:  
              $( "#twin_status" ).text("...");
              $( "#twin_status" ).css("color","#fff");
              //console.log("setting class "+" neutral");
              //$( "#twin_status" ).toggleClass("neutral");
              break; 
              
    }
    
       
}


function replace_minifigure(event_, speaker){
 //EVENT2 HAS SUBEVENTS
    // fade out
    $( "#minifigure_image" ).animate({
       opacity: 0,
       "margin-left": "-50",
     }, 500, function() {
       // Animation complete -> Replace image

           //EVENT2 HAS SUBEVENTS
           $( "#minifigure_image" ).attr('src', speaker);
           // fade in minifigure
           $( "#minifigure_image" ).animate({
           opacity: 1,
           "margin-left": "0",
           }, 500, function(){
           // fade in speech container
           $( "#container_speach" ).animate({
                   opacity: 1,
           }, 500, function(){ 
                                   last_animation_ready=true;     
                             });
  
                           });
  
                       });
                       
                              
                        
}

// Replace the Instructions and the speaker
function replace_instruction(event_, subevent){
   // fade out
  //last_animation_ready=false;
  $( "#container_speach" ).animate({
    opacity: 0,
  }, 500, function() {
  // Animation complete
  	if (event_=="event2"){
                 var minifigure=instruction[event_][subevent][2][1];
                   	 $( "#container_speach").text(instruction[event_][subevent][0]+ asset["a"+current_asset.toString()][1] +instruction[event_][subevent][1]);
  	                 $( "#speaker" ).text(instruction[event_][subevent][2][0]);
                     //cerrent_instruction=instruction[event_][subevent][0];
           }else{
                  var minifigure=instruction[event_][1][1];
                     $( "#container_speach").text(instruction[event_][0]);
  	                 $( "#speaker" ).text(instruction[event_][1][0]);
  	                 //cerrent_instruction=instruction[event_][0];
           }
           
           if (!(current_speaker==minifigure)){
           current_speaker=minifigure;
           replace_minifigure(event_, minifigure);
           }else{
           //last_animation_ready=true;
            $( "#container_speach" ).animate({
                   opacity: 1,
             }, 500);
               }

     });           
}


// Replace Source of iFrame
function replace_iframe(current_url){
	$("#ain").attr('src', current_url); 
}

function replace_screen(src){
if (!(last_image==src)){
    
    $('#'+last_image).css('visibility','hidden');
    $('#'+src).css('visibility','visible');
    last_image=src;
    
    /*$( "#screenshot" ).attr('src', src);
    //$( "#screenshot" ).attr('src', img);
    */
    
    
}
}


//TODO_: implement this function in a loop
function install_pump(event_,asset_rfid_id, pimped){
     timeout_e1=null;
     $("#button_next").css("visibility","visible");
     $("#button_previous").css("visibility","hidden");
     var asset_ = "a"+asset_rfid_id.toString();
     console.log("setting current_asset "+pimped);
     current_asset=asset_rfid_id;
	 replace_asset(asset_, pimped);   
     replace_marketing(event_,"e0");
     replace_instruction(event_,"e0");
     replace_screen(instruction[event_]["e0"][3]);
     console.log("sleeping...")
     timeout = setTimeout(function(){install_pump_e1(event_);}, 10000);

}


function install_pump_e1(event_){
    //$("#button_next").css("visibility","hidden");
    $("#button_previous").css("visibility", "visible");
    replace_marketing(event_,"e1");
    replace_screen(instruction[event_]["e1"][3]);
    console.log("setting asset installed");
    update_asset_status(2);
    //one pixel image trick to create a http transaction
    
    //inform backend that the installation process is completed
    timeout_e1 = setTimeout(function(){
    var image = new Image();
    image.src = "/asset_installed/";
    }, 10000);
    
    
    //update_asset_status(2);
    //wait(5000);
    //installed=true;
    
    /*
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", "/asset_installed/", true ); // false for synchronous request
    xmlHttp.send( null );
    */
  
    /*setTimeout(function(){
       console.log(event_backup.length);
       for (var i = 0; i < event_backup.length; i++) {
        console.log(event_backup[i].number);
        reset_all_texts(event_backup[i].number,event_backup[i].asset_rfid,event_backup[i].pimp);
       }     
      installed=true;
      
    }, 10000);
    */
  
   }

   

/*
function install_pump_e2(event_){
   console.log("sleeping...")
   //wait(6000);
   //replace_screen(instruction[event_]["e2"][2]);
   $( "#marketing_headline" ).text(marketing[event_]["e2"][0]);
   $( "#marketing_text" ).text(marketing[event_]["e2"][1]);
   $( "#speaker" ).text(instruction[event_]["e2"][1][0]);
   $( "#container_speach").text(instruction[event_]["e2"][0]);
   //update the rasp, asset installed
   $.ajax({
            type: 'GET',
            url: "/asset_installed/",
            data: 0,
            success: function (data) {
              
             }
        });
   
}
*/

function reset_all_texts(event_nr, asset_rfid_id, pimped){
//event 8 does not change any instructions/marketing or speaker
var event_="event"+event_nr.toString();
switch (event_nr){
case 8:
     break;
case 2:
     installed=false;
     install_pump(event_, asset_rfid_id, pimped);
     
     break;
case 10:
     replace_instruction(event_);
     break;

case 6:
    var asset_ = "a"+asset_rfid_id.toString();
    //$("#asset_image").one("load", function() {
        replace_asset(asset_, true);
        replace_marketing(event_);
	    replace_instruction(event_);
	    update_asset_status(event_nr);
	    replace_screen(instruction[event_][2]);
	    //$( "#screenshot" ).attr('src', instruction[event_][2]);
     //}).attr("src", asset[asset_][3]);
       break;
case 7:
 var asset_ = "a"+asset_rfid_id.toString();
 //$("#asset_image").one("load", function() {
    //replace_asset_boosted(asset_);
     //$("#screenshot").one("load", function() {
	   //replace_marketing(event_);
	   replace_asset(asset_, false);
	   replace_instruction(event_);
	   update_asset_status(event_nr);
	   replace_screen(instruction[event_][2]);
	   //$( "#screenshot" ).attr('src', instruction[event_][2]);
       //replace_asset(asset_);
     //}).attr("src", "static/img/"+ instruction[event_][2]);
   //}).attr("src", asset[asset_][2]);
       break;
case 3:
      console.log("event 3");
      replace_marketing(event_);
	  replace_instruction(event_);
	  update_asset_status(event_nr);
	  break;
case 5:
      replace_instruction(event_);
      update_asset_status(event_nr);
      break;
case 1:
      //no asset on the rfid 
	  var asset_ = "a"+"000";
	  update_asset_status(event_nr);
	  replace_asset(asset_);
	  replace_marketing(event_);
	  replace_instruction(event_);
	  console.log(instruction[event_][2]); 
	  replace_screen(instruction[event_][2]);
      break;
case 0:
      //INNITIAL SETUP
	  var asset_ = "a"+"000";
	  update_asset_status(event_nr);
	  replace_instruction(event_);
	  replace_screen(instruction[event_][2]);
      break;
case 11:
case 12:
      console.log("event 11");
      replace_instruction(event_);
	  //update_asset_status(event_nr);
	  break;

default:
    replace_marketing(event_);
	replace_instruction(event_);
	update_asset_status(event_nr);
	replace_screen(instruction[event_][2]);  
    
} 
console.log("all texts reset");
}

function stop_demo(){
        $("#container_speach").text("stopping...");
        $.ajax({
            type: 'GET',
            url: "/stop/",
            data: 0,
            async: false,
            success: function (data) {
             $("#container_speach").text("stopped");
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

function preload(arrayOfImages) {
   for (index = 0; index < arrayOfImages.length; ++index) {
      $('<img />').attr('src',arrayOfImages[index]).attr('id',"screenshot"+(index+1)).appendTo('#container_iframe').css('visibility','hidden');
   }
}


// INITIAL SETUP
$( document ).ready(function() {
	console.log("document loaded");
	//start_demo();
	//test
	//reset_all_texts(0, 0, 0);
	screen_mode("screenshot");
	
	preload(["static/img/screenshot1.jpg","static/img/screenshot2.jpg","static/img/screenshot3.jpg","static/img/screenshot4.jpg"]);
	
	if ("WebSocket" in window){
           //var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           var ws = new WebSocket("ws://0.0.0.0:5000/websocket");
           //var messagecount = 0;
           start_demo();
           ws.onmessage = function(evt) {
              messagecount += 1;
              var event = JSON.parse(evt.data);
              event_nr=event.event;
              asset_rfid_id=event.asset_rfid_id;
              pimped=event.pimped;
              //while (!(installed==true)){
              //}
              if(!(current_event==event_nr)){
                if (current_event==2){
                  $("#button_previous").css("visibility", "hidden");
                  $("#button_next").css("visibility", "hidden");
                 }
                 reset_all_texts(event_nr, asset_rfid_id, pimped);
                 current_event=event_nr;
                 console.log(event_nr);
             } 
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

$("#button_reset").click(function(evt) {
  stop_demo();
  $("#container_speach").text("reloading...");
  location.reload();
     });
  
$("#button_next").click(function(evt) {
        if(current_event==2){
        console.log("clearing");
        //paused=true;
        clearTimeout(timeout);
        //var event_="event"+current_event.toString();
        if(!(timeout_e1==null)){
          clearTimeout(timeout_e1);
          var image = new Image();
          image.src = "/asset_installed/";
          $("#button_previous").css("visibility", "hidden");
          $("#button_next").css("visibility", "hidden");
         }else{
           install_pump_e1("event2");
              }
        }
     });

$("#button_previous").click(function(evt) {

       if(current_event==2){
        console.log("clearing");
        if(!(timeout_e1==null)){
          clearTimeout(timeout_e1);
          timeout_e1==null;
         }
        //paused=true;
        //clearTimeout(timeout);
        //var event_="event"+current_event.toString();
        install_pump("event2",current_asset);
        
        
        
        }
     });


//STOP EXECUTION ON RELOAD 
window.onbeforeunload = function(event){ 
           stop_demo();
    };     


