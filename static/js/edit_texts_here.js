// Use the fields in the following arrays to edit the information that can be displayed on screen//
/*
EVENTS
1 - installation of  a new aset
2 - new asset installed, show new asset information
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
 marketing.event0  = ["Welcome", "AIN is really great because the installation of new assets is really simple. You just connect your device to the network and all the necessary data is directly pulled from the manufacturer. No more need for updates and no more fear of using outdated software. With AIN you are always on the safe side!"];
 marketing.event1 = ["Installation of a new asset", "AIN is really great because the installation of new assets is really simple. You just connect your device to the network and all the necessary data is directly pulled from the manufacturer. No more need for updates and no more fear of using outdated software. With AIN you are always on the safe side!"];
 marketing.event2 = ["Asset Installed"," Marketting Asset Installed"];
 marketing.event3 = ["Repairing of a broken machine", "Information about how to repari a broken machine can be shared"];
 marketing.event4 = ["Issue of a service bulletin","Whenever there is an update from the manufacturer, all operators get notified"];
 marketing.event5 = ["Repaired", "Information about how to repari a broken machine can be shared"];
 marketing.event6 = ["Asset pimped!","You just pimped the asset"];
 marketing.event7 = ["Asset unpimped","You just unpimped the asset"];
 
// Speaker arrays [Name, Mini-figure image name] //
speaker = {};
speaker.manufacturer=["Manufacturer", "minifigure2.png"];
speaker.operator=["Operator", "minifigure1.png"];
speaker.service=["Service provider", "minifigure3.png"];

// Instruction arrays [Text] //
instruction = {};
instruction.event0 = ["Here you will see the instructions for the asset handling",speaker.manufacturer];
instruction.event1 = ["Operator can by an asset by choosing the desired asset and placing it on the operators facilities",speaker.manufacturer];
instruction.event2 = ["Wow, the asset is installed",speaker.operator];
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
