/*
EVENTS
 #0 - initial setup
 #1 - no asset on rfid
 #2 - assert bought
    2.e0 - asset registration
    2.e1 - asset synchronisation
 #3 - asset breaks
 #4 - inform user about the service bulletin functionality
 #5 - asset is repaired by the service car
 #6 - boost the asset
 #7 - unboost the asset
 #8 - 
 #9 - manufacturer wants to activat the bulletin
 #10 - remind to boost the asset
 #11 - remind to remove the service car form the manufacturer's facilities
 #12 - thanks for removing the car
*/

var paused=false;
var backup_event={nr:null,asset:null,pimp:null};
var timeout;
var timeout_e1=null;
var installed=true;
var innitial_asset="000";
var current_asset=innitial_asset;
var current_event;
var last_image="screenshot1";
var current_speaker;
var last_animation_ready=true;
var event_sequence_for_emergency=[2,9,4,10,6,3,5,11,12,7];
var current_emergency_event_index=0;
var emergency_mode_event_2=false;
var emergency_mode_flow_control_klicked_next;

/*
function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}
*/

// Switch between iFrame and screenshots
function screen_mode(mode){
  console.log("changing screenmode to "+mode);
 $("#container_iframe").empty(); // clears iframe container
 switch(mode){
    case "screenshot":  $("#container_iframe").append("<img id='screenshot1a000' src='static/img/screenshot1.jpg' alt='Screenshot missing'>");
                        console.log("changed to screenshot");
          break;
    case "iframe": $("#container_iframe").append("<iframe id='ain' src='http://veui5infra.dhcp.wdf.sap.corp:8080/sapui5-sdk-dist/explored.html#/sample/sap.uxap.sample.AlternativeProfileObjectPageHeader/preview'></iframe>");
          console.log("changed to iframe");
          break;
    default: $("#container_iframe").append("<img id='screenshot1' src='static/img/screenshot1.jpg' alt='Screenshot missing'>");   
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
    //current_asset=asset_;
    console.log(asset_);
    console.log(pimped);
	$( "#twin_id" ).text(assets[asset_][0]);
	$( "#twin_model" ).text(assets[asset_][1]);
	if (pimped==true){
	  var src = $('#'+asset_+'x').attr('src');
	  $( "#asset_image" ).animate({
      opacity: 0,
     }, 500, function(){
     
	     $( "#asset_image" ).attr('src', src);
	     // fade in
	     $( "#asset_image" ).animate({opacity: 1,}, 500);
	     }); 
	  $( "#twin_id" ).text(assets[asset_][3]);
	}else{
	  var src = $('#'+asset_).attr('src');
	  $( "#asset_image" ).animate({
      opacity: 0,
      }, 500, function(){
	  $( "#asset_image" ).attr('src', src);
	  $( "#asset_image" ).animate({opacity: 1,}, 500);
	  
	   }); 
	  $( "#twin_id" ).text(assets[asset_][0]);
	  
	}
}


//updating the assetsstatus
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
           var src = $('#'+speaker).attr('src');
           $( "#minifigure_image" ).attr('src', src);
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
                   	 $( "#container_speach").text(instruction[event_][subevent][0]+ assets["a"+current_asset.toString()][1] +instruction[event_][subevent][1]);
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
    console.log(src+"a"+current_asset);
    $('#'+last_image+"a"+current_asset).css('visibility','hidden');
    //$('#'+src).css('visibility','visible');
    $('#'+src+"a"+current_asset).css('visibility','visible');
    last_image=src;
    
    /*$( "#screenshot" ).attr('src', src);
    //$( "#screenshot" ).attr('src', img);
    */
    
    
}
}


//TODO_: implement this function in a loop
function install_pump(event_,asset_rfid_id, pimped){
     timeout_e1=null;
     if (!(current_event==15)) {
        $("#button_next").css("visibility", "visible");
        $("#button_previous").css("visibility", "hidden");
     }
     var asset_ = "a"+asset_rfid_id.toString();
     console.log("setting current_assets "+pimped);
     //current_asset=asset_rfid_id;
	 replace_asset(asset_, pimped);   
     replace_marketing(event_,"e0");
     replace_instruction(event_,"e0");
     replace_screen(instruction[event_]["e0"][3]);
     console.log("sleeping...")
     timeout = setTimeout(function(){
     install_pump_e1(event_);
     }, 10000);

}


function install_pump_e1(event_){
    $("#button_previous").css("visibility","visible");
    replace_marketing(event_,"e1");
    replace_screen(instruction[event_]["e1"][3]);
    //console.log("setting assetsinstalled");
    update_asset_status(2);
    //one pixel image trick to create a http transaction
    //inform backend that the installation process is completed
    timeout_e1 = setTimeout(function(){
    //var image = new Image();
    //image.src = "/asset_installed/";
    installed=true;
        if (!(current_event==15)) {
            $("#button_previous").css("visibility", "hidden");
            $("#button_next").css("visibility", "hidden");
        }
        emergency_mode_event_2=false;
        $("#emergency").css("visibility", "hidden");
        if (!(backup_event.nr==null)) {
           reset_all_texts(backup_event.nr, backup_event.asset, backup_event.pimp);
           current_event = backup_event.nr;
       }

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
   //update the rasp, assetsinstalled
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
    console.log("event 2 "+asset_rfid_id);
     current_asset=asset_rfid_id;
     install_pump(event_, asset_rfid_id, pimped);
     if (current_event==15) {
         emergency_mode_event_2 = true;
     }
     break;

case 10:
     replace_instruction(event_);
     break;

case 6:
    var asset_ = "a"+asset_rfid_id.toString();
    //$("#asset_image").one("load", function() {
        console.log("else "+event_)
        replace_asset(asset_, true);
        replace_marketing(event_);
	    replace_instruction(event_);
	    update_asset_status(event_nr);
	    replace_screen(instruction[event_][2]);
	    //$( "#screenshot" ).attr('src', instruction[event_][2]);
     //}).attr("src", assets[asset_][3]);
       break;
case 7:
 var asset_ = "a"+asset_rfid_id.toString();
	   replace_asset(asset_, false);
	   replace_instruction(event_);
	   update_asset_status(event_nr);
	   replace_screen(instruction[event_][2]);
       break;
case 3:
      console.log("event 3");
      replace_marketing(event_);
	  replace_instruction(event_);
	  update_asset_status(event_nr);
	  replace_screen(instruction[event_][2]);
	  break;
case 5:
      replace_instruction(event_);
      update_asset_status(event_nr);
      //replace screen only
      if (!(current_asset==innitial_asset)){
          replace_screen(instruction[event_][2]);
      }else{
          replace_screen("screenshot1");
      }
      break;
case 1:
      //no assetson the rfid
	  update_asset_status(event_nr);
      replace_screen(instruction[event_][2]);
	  replace_asset("a"+innitial_asset);
      current_asset=innitial_asset;
	  replace_marketing(event_);
	  replace_instruction(event_);
	  console.log(instruction[event_][2]);
      break;
    case 0:
      //INNITIAL SETUP
      $("#emergency").css("visibility", "visible");
	  update_asset_status(event_nr);
	  replace_instruction(event_);
      replace_screen(instruction[event_][2]);
	  if (!(current_asset==innitial_asset)){
	      replace_asset("a"+innitial_asset);
          current_asset=innitial_asset;
	  }
      break;
case 11:
case 12:
      console.log("event 11");
      replace_instruction(event_);
	  //update_asset_status(event_nr);
	  break;
case 15:
      console.log("event 15");
      //$("#button_previous").css("visibility", "visible");
      $("#button_next").css("visibility", "visible");

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

function preload(arrayOfImages, asset) {
   for (index = 0; index < arrayOfImages.length; ++index) {
      //$('<img />').attr('src',arrayOfImages[index]).attr('id',"screenshot"+(index+1)).appendTo('#container_iframe').css('visibility','hidden');
      $('<img />').attr('src',arrayOfImages[index]).attr('id',"screenshot"+(index+2)+asset).appendTo('#container_iframe').css('visibility','hidden');
   }
}
function preload_minifigures(Image) {
      $('<img />').attr('src',"static/img/"+Image+".png").attr('id',Image).appendTo('#container_preload').css('visibility','hidden');
}
function preload_pumps(arrayOfImages, asset) {
      //$('<img />').attr('src',arrayOfImages[index]).attr('id',"screenshot"+(index+1)).appendTo('#container_iframe').css('visibility','hidden');
      $('<img />').attr('src',arrayOfImages[0]).attr('id',asset).appendTo('#container_preload');
      $('<img />').attr('src',arrayOfImages[1]).attr('id',asset+"x").appendTo('#container_preload'); 
}


// INITIAL SETUP
$( document ).ready(function() {
	console.log("document loaded");
	screen_mode("screenshot");
	for(var asset in assets)
	   {
          preload(assets[asset][assets[asset].length-1],asset);
          preload_pumps(assets[asset][2],asset);
       }
    for(var minifigure in speaker)
	   {
         preload_minifigures(speaker[minifigure][speaker[minifigure].length-1]);
       }
	
	if ("WebSocket" in window){
           //var ws = new WebSocket("ws://192.168.2.2:5000/websocket");
           var ws = new WebSocket("ws://0.0.0.0:5000/websocket");
           var messagecount = 0;
           start_demo();
           ws.onmessage = function(evt) {
              messagecount += 1;
              var event = JSON.parse(evt.data);
              event_nr=event.event;
              asset_rfid_id=event.asset_rfid_id;
              pimped=event.pimped;
               //evoid repeating same event
              if(!(current_event==event_nr)){
                 //if event 2 is not ready with installing the asset
                  //installed is set to true when asset is intalled - event 2 is ready
                 if (installed==false){
                   //backing up incoming events during the installation for the later execution
                   if((event_nr==9 || event_nr==3 || event_nr==10 || event_nr==14||event_nr==15||event_nr==7)) {
                       console.log("saving");
                       console.log(event_nr);
                       current_event = event_nr;
                       backup_event = {nr: event_nr, asset: asset_rfid_id, pimp: pimped};
                   }else if ( event_nr==1 || event_nr==0) {
                       clearTimeout(timeout);
                       clearTimeout(timeout_e1);
                       installed = true;
                       current_event = event_nr;
                       reset_all_texts(event_nr, asset_rfid_id, pimped);


                   }
                       //if asset is broken during the installation and than repaired during the installation, the repair event should not be saved
                   else if (event_nr==5){
                       if (asset_rfid_id==current_asset) {
                           console.log("setting backup to null");
                           backup_event={nr:null, asset:null, pimp:null};

                       }else{
                           //if the asset is changed during the installation of another asset
                           console.log("saving");
                           console.log(event_nr);
                           current_event=event_nr;
                           backup_event={nr:event_nr, asset:asset_rfid_id, pimp:pimped};
                       }
                 }
                 } else{
                     console.log("not saving");
                     console.log(event_nr);
                     console.log(asset_rfid_id);
                     current_event=event_nr;
                     reset_all_texts(event_nr, asset_rfid_id, pimped);
                 }
                 
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
        if(current_event==2 || (emergency_mode_event_2==true && current_event==15)){
        console.log("clearing");
        //paused=true;
        clearTimeout(timeout);
        //var event_="event"+current_event.toString();
        if(!(timeout_e1==null)){
          clearTimeout(timeout_e1);
          //var image = new Image();
          //image.src = "/asset_installed/";
           installed=true;
            if (!(current_event==15)) {
                $("#button_previous").css("visibility", "hidden");
                $("#button_next").css("visibility", "hidden");
                $("#emergency").css("visibility", "hidden");

            }else
            {
                 emergency_mode_event_2 = false;
                 reset_all_texts(event_sequence_for_emergency[current_emergency_event_index], 215, false);
                 current_emergency_event_index = current_emergency_event_index+1;
                 emergency_mode_flow_control_klicked_next=true;
            }
          if (!(backup_event.nr==null)) {
              reset_all_texts(backup_event.nr, backup_event.asset, backup_event.pimp);
              current_event = backup_event.nr;
          }
         }else{
           install_pump_e1("event2");
              }
        }
    else if (current_event==15 && emergency_mode_event_2==false) {
          if (current_emergency_event_index<event_sequence_for_emergency.length) {
              console.log(current_emergency_event_index);
              reset_all_texts(event_sequence_for_emergency[current_emergency_event_index], 215, false);
              current_emergency_event_index = current_emergency_event_index+1;
              emergency_mode_flow_control_klicked_next=true;
              if (current_emergency_event_index==event_sequence_for_emergency.length-1){
                   //last event
                   $("#button_next").css("visibility", "hidden");
              }

          }else{
              $("#button_next").css("visibility", "hidden");
          }

        }
     });

$("#button_previous").click(function(evt) {
       if(current_event==2 || (emergency_mode_event_2==true && current_event==15)){
        console.log("clearing");
        if(!(timeout_e1==null)){
          clearTimeout(timeout_e1);
          timeout_e1==null;
         }
           install_pump("event2",current_asset);
           $("#button_previous").css("visibility", "hidden");
        }
    else if (current_event==15 && emergency_mode_event_2==false){
          if (!(current_emergency_event_index<=0)){
              current_emergency_event_index = current_emergency_event_index - 1;
              if (emergency_mode_flow_control_klicked_next==true){
                  current_emergency_event_index = current_emergency_event_index - 1;
              }
              emergency_mode_flow_control_klicked_next=false;
              if (current_emergency_event_index==0){
                  $("#button_previous").css("visibility", "hidden");
              }
              console.log("Step back "+current_emergency_event_index);
              reset_all_texts(event_sequence_for_emergency[current_emergency_event_index], 215);
              //put back the "button_next" if there are next events
              if (current_emergency_event_index<event_sequence_for_emergency.length && $(button_next).css("visibility")=="hidden" ){
                   $("#button_next").css("visibility", "visible");
              }

          }else{
              $("#button_previous").css("visibility", "hidden");
          }
       }
     });

$("#emergency").click(function(evt) {
       console.log("Emergency mode");
       var image = new Image();
       image.src = "/emergency/";
       $("#emergency").css("visibility", "hidden");


     });


//STOP EXECUTION ON RELOAD 
window.onbeforeunload = function(event){ 
           stop_demo();
    };     


