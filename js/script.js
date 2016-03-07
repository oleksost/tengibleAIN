

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
	$( "#asset_image" ).attr('src', "img/"+asset[current_asset][3]+".gif"); 
}


// Replace the Text of the Instructions
function replace_instruction(current_instruction){
	$( "#container_speach").text(instruction[current_instruction][0]);
}


// Replace Source of iFrame
function replace_iframe(current_url){
	$("#ain").attr('src', current_url); 
}



// Reset all Values
function reset_all_texts(){
	replace_marketing(initial_marketing);
	replace_asset(initial_asset);
	replace_instruction(initial_instruction);
	replace_iframe(initial_url);
	console.log("all texts reset");
}

// TRY TO CALL THIS FUNCTION VIA THE RASPBERRY PI
function python_test(){
	console.log("python test successfull");
	replace_marketing("m2");
	replace_asset("a3");
	replace_instruction("i1");
	replace_iframe("http://www.w3schools.com/");
}

// INITIAL SETUP
$( document ).ready(function() {
	console.log("document loaded");
	reset_all_texts();
});

