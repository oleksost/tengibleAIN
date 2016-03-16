// Use the fields in the following arrays to edit the information that can be displayed on screen//
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

// Asset Arrays [ID, MODEL, STATUS, IMAGEFILE], RFID as identifier: e.g. a215 has RFID id 215//
 asset = {};
 asset.a000 = ["none", "none", "unknown", ""];	
 asset.a215 = ["ID 1111 - 1x", "seawater pump", "working", "asset1"];	
 asset.a138 = ["id2", "motor", "installed", "asset2"];
 asset.a133 = ["id3", "battery", "broken", "asset2"];


// Marketing Arrays [HEADLINE, TEXT] //
 marketing = {}; 
 //initial marketing
 marketing.event0  = ["Welcome", "AIN is really great because the installation of new assets is really simple. You just connect your device to the network and all the necessary data is directly pulled from the manufacturer. No more need for updates and no more fear of using outdated software. With AIN you are always on the safe side!"];
 marketing.event1 = ["Installation of a new asset", "AIN is really great because the installation of new assets is really simple. You just connect your device to the network and all the necessary data is directly pulled from the manufacturer. No more need for updates and no more fear of using outdated software. With AIN you are always on the safe side!"];
 marketing.event2 = ["Asset Installed"," Marketting Asset Installed"];
 marketing.event3 = ["Repairing of a broken machine", "Information about how to repari a broken machine can be shared"];
 marketing.event4 = ["Issue of a service bulletin","Whenever there is an update from the manufacturer, all operators get notified"];
 marketing.event5 = ["Repaired", "Information about how to repari a broken machine can be shared"];
 marketing.event6 = ["Pimp the asset","How cool, asset can now be pimped"];
 marketing.event7 = ["Asset pimped!","You just pimped the asset"];
 
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
instruction.event4 = ["New update is issued to the service bulletin",speaker.manufaturer];
instruction.event5 = ["Enjoy your asset, it is repaired and working well",speaker.service];
instruction.event6 = ["Bring the asset to he next level - pimp it by installing the asset booster",speaker.manufacture];
instruction.event7 = ["Congratulations, your asset is now boosted",speaker.service];




