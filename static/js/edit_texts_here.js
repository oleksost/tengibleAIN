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
 asset.a000 = ["none", "none", ""];	
 asset.a215 = ["ID 1111 - 1x", "seawater pump", "asset1.png"];	
 asset.a138 = ["ID 2135 - 25x", "motor", "asset2.png"];
 asset.a133 = ["ID 2607 - 5xd", "battery", "asset2.png"];


// Marketing Arrays [HEADLINE, TEXT] //
 marketing = {}; 
 //initial marketing
 marketing.event0 = ["Connecting Operators and Manufacturers", "The Asset Intelligence Network is a great product to share inforamtion between all participants. Move the yellow Lego objects to see what is possible."];
 marketing.event1 = ["Connecting Operators and Manufacturers", "The Asset Intelligence Network is a great product to share inforamtion between all participants. Move the yellow Lego objects to see what is possible."];
 marketing.event2 = {}
 marketing.event2.e0=["New Asset Installation", "Registering new assets with the manufacturer has never been easier. Simply scan the code on the machine and sync the data between you and the manufacturer."];
 marketing.event2.e1=["New Asset Installation", "Synching usage data between operators and manufacturers offers entirely new business models, such as Asset as a Service, on the manufacturer side. For the operator it guarantees best possible service and maintenance before assets break."];
 marketing.event2.e2=["New Asset Installation", "Synching usage data between operators and manufacturers offers entirely new business models, such as Asset as a Service, on the manufacturer side. For the operator it guarantees best possible service and maintenance before assets break."];

 marketing.event3 = ["Repairing of a broken machine", "Information about how to repari a broken machine can be shared"];
 marketing.event4 = ["Issue of a service bulletin","Whenever there is an update from the manufacturer, all operators get notified"];
 marketing.event5 = ["Repaired", "Information about how to repari a broken machine can be shared"];
 marketing.event6 = ["Asset pimped!","You just pimped the asset"];
 marketing.event7 = ["Asset unpimped","You just unpimped the asset"];
 
// Speaker arrays [Name, Mini-figure image name] //
speaker = {};
speaker.manufacturer=["Manufacturer", "minifigure1.png"];
speaker.operator=["Operator", "minifigure3.png"];
speaker.service=["Service provider", "minifigure2.png"];

// Instruction arrays [Text] //
instruction = {};
instruction.event0 = ["Here you will see the instructions for the asset handling",speaker.manufacturer];
instruction.event1 =["I need a new pump. Let’s get one from the factory and place it on my plant.",speaker.operator, "img1.png"];

//Installation
instruction.event2 = {};
instruction.event2.e0 =["Nice Seawater Pump! I’ll connect it to the Manufacturer’s network.",speaker.operator, "img1.png"];
instruction.event2.e1 =["Nice Seawater Pump! I’ll connect it to the Manufacturer’s network.",speaker.operator, "img2.png"];
instruction.event2.e2 =["Based on your machine usage I just improved the service agreement. Please install the update when you are ready.",speaker.manufacturer, "img2.pmg"];

instruction.event3 = ["Your asset is broken! IN order to repair it place the service-car on the operator's platform",speaker.service];
instruction.event4 = ["New update is issued to the service bulletin", speaker.manufacturer];
instruction.event5 = ["Enjoy your asset, it is repaired and working well",speaker.service];
instruction.event6 = ["Congratulations, your asset is now boosted",speaker.service];
//instruction.event7 = ["Congratulations, your asset is now boosted",speaker.service];

/*
HINTS
h1 - clean the hint display
h2 - bulletin should be moved to the manufacturer for the verification at the beginning of the demo
h3 - service car should be moved back to the service station
h4 - reminder to bring back the car
h5 - asset can be pimped
h6 - bulleting is activated and should be brought to the operator
*/
hints = {};
hints.h1 = [""];
hints.h2 = ["To receive new updates verify the bulletin at manufacturers facilities"];
hints.h3 = ["Please, move the service car back to the service station"];
hints.h4 = ["You need to move the car away from the operators facilities before repairing the asset again"];
hints.h5 = ["You can pimp your asset by moving the booster from the service station and placing it to the asset"];
hints.h6 = ["Bulleting activated, bring it to the operator"];
