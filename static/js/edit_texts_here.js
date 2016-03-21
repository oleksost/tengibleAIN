// Use the fields in the following arrays to edit the information that can be displayed on screen//
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
6 - asset is pimped 
7 - sset is unpimped
8 - display a new hint
*/

 

// Asset Arrays [ID, MODEL, IMAGEFILE], RFID as identifier: e.g. a215 has RFID id 215//
 asset = {};
 asset.a000 = ["...", "...", new Image().src="static/img/asset0.png",""];
 asset.a215 = ["ID 1111 - 1x", "seawater pump", new Image().src="static/img/asset1.gif", new Image().src="static/img/asset1x.png"];	
 asset.a138 = ["ID 2135 - 25x", "motor", new Image().src="static/img/asset2.png",new Image().src="static/img/asset2x.png"];
 asset.a133 = ["ID 2607 - 5xd", "pump", new Image().src="static/img/asset3.png",new Image().src="static/img/asset3x.png"];


// Marketing Arrays [HEADLINE, TEXT] //
 marketing = {};  
 //initial marketing
 marketing.event0 = ["Connecting Operators and Manufacturers", "The Asset Intelligence Network is a great product to share inforamtion between all participants. Move the yellow Lego objects to see what is possible."];
 marketing.event1 = ["Connecting Operators and Manufacturers", "The Asset Intelligence Network is a great product to share inforamtion between all participants. Move the yellow Lego objects to see what is possible."];
 marketing.event2 = {}
 marketing.event2.e0=["New Asset Installation", "Registering new assets with the manufacturer has never been easier. Simply scan the code on the machine and sync the data between you and the manufacturer."];
 marketing.event2.e1=["New Asset Installation", "Synching usage data between operators and manufacturers offers entirely new business models, such as Asset as a Service, on the manufacturer side. For the operator it guarantees best possible service and maintenance before assets break."];
 //marketing.event2.e2=["New Asset Installation", "Synching usage data between operators and manufacturers offers entirely new business models, such as Asset as a Service, on the manufacturer side. For the operator it guarantees best possible service and maintenance before assets break."];
 marketing.event9 = ["New Asset Installation","Synching usage data between operators and manufacturers offers entirely new business models, such as Asset as a Service, on the manufacturer side. For the operator it guarantees best possible service and maintenance before assets break."];

 marketing.event3 = ["Error Handling", "Errors can be quickly detected and fixed before assets break. Connected third party or in-house service providers receive all necessary information such as required spare parts, maintenance and safety instructions before they set off for a one-stop service. This safes time, money and nerves."];
 marketing.event4 = ["Service Bulletins","Updated product, maintenance or service instructions can be quickly shared within the network. AIN helps to avoid duplicates and local copies of outdated information. This keeps all processes simple and lean."];
 marketing.event5 = ["Error Handling", "Errors can be quickly detected and fixed before assets break. Connected third party or in-house service providers receive all necessary information such as required spare parts, maintenance and safety instructions before they set off for a one-stop service. This safes time, money and nerves.	"];
 marketing.event6 = ["Performance Improvement","Changing the asset configuration, e.g. to improve the performance is mostly unnoticed by the manufacturer. However, it can affect the guarantee and service agreements. With the Asset Intelligence Network even third party service companies can log and share configurational changes."];
 marketing.event7 = ["Asset unpimped","You just unpimped the asset"];
 
 
// Speaker arrays [Name, Mini-figure image name] //
speaker = {};
speaker.manufacturer=["Manufacturer", new Image().src="static/img/minifigure1.png"];
speaker.operator=["Operator", new Image().src="static/img/minifigure3.png"];
speaker.service=["Service provider", new Image().src="static/img/minifigure2.png"];

// Instruction arrays [Text] //
instruction = {};
instruction.event0 = ["I need a new asset. Let’s get one from the factory and place it on my plant.",speaker.operator, new Image().src="static/img/screenshot1.jpg"];
instruction.event1 = ["Can I offer you another asset? Please don’t forget to put the performance improving part back to the service.",speaker.manufacturer, new Image().src="static/img/screenshot1.jpg"];

//Installation
instruction.event2 = {};
instruction.event2.e0 =["Nice ", "! I’ll connect it to the Manufacturer’s network.",speaker.operator, new Image().src="static/img/screenshot2.jpg"];
instruction.event2.e1 =["Nice ", "! I’ll connect it to the Manufacturer’s network.",speaker.operator, new Image().src="static/img/screenshot3.jpg"];
//instruction.event2.e2 =["Based on your machine usage I just improved the service agreement. Please install the update when you are ready.",speaker.manufacturer, "screenshot3.jpg"];

instruction.event3 = ["Drive my truck onto the operator’s site to fix this!",speaker.service];
instruction.event9 = ["Based on your machine usage I just improved the service agreement. Please install the update when you are ready.",speaker.manufacturer, new Image().src="static/img/screenshot3.jpg"];
instruction.event4 = ["Cool! You are a great help. Updates will be now installed automatically", speaker.operator, new Image().src="static/img/screenshot4.jpg"];
instruction.event5 = ["Thanks, this was a quick fix. The truck may now leave my site",speaker.operator];
instruction.event6 = ["Thanks, the new component increased the performance by 23%!",speaker.operator,new Image().src="static/img/screenshot5.jpg"];
instruction.event7 = ["Sorry to hear, you didn’t like it. Can do something else for you?",speaker.service,new Image().src="static/img/screenshot5.jpg"]; 
instruction.event10 = ["This asset could do even better. Add my new component to improve the performance.",speaker.service, new Image().src="static/img/screenshot4.jpg"];

/*
HINTS
h1 - clean the hint display
h2 - bulletin should be moved to the manufacturer for the verification at the beginning of the demo
h3 - service car should be moved back to the service station
h4 - reminder to bring back the car
h5 - asset can be pimped
h6 - bulleting is activated and should be brought to the operator
hints = {};
hints.h1 = [""];
hints.h2 = ["To receive new updates verify the bulletin at manufacturers facilities"];
hints.h3 = ["Please, move the service car back to the service station"];
hints.h4 = ["You need to move the car away from the operators facilities before repairing the asset again"];
hints.h5 = ["You can pimp your asset by moving the booster from the service station and placing it to the asset"];
hints.h6 = ["Based on your machine usage I just improved the service agreement. Please install the update when you are ready.",speaker.manufacturer, "screenshot3.jpg"];
*/