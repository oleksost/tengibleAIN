// Use the fields in the following arrays to edit the information that can be displayed on screen


// Asset Arrays [ID, MODEL, STATUS, IMAGEFILE] //
 asset = {}; 
 asset.a1 = ["ID 1111 - 1x", "seawater pump", "working", "asset1"];
 asset.a2 = ["id2", "motor", "installed", "asset2"];
 asset.a3 = ["id3", "battery", "broken", "asset2"];


// Marketing Arrays [HEADLINE, TEXT] //
 marketing = {}; 
 marketing.m1 = ["Installation of a new asset", "AIN is really great because the installation of new assets is really simple. You just connect your device to the network and all the necessary data is directly pulled from the manufacturer. No more need for updates and no more fear of using outdated software. With AIN you are always on the safe side!"];
 marketing.m2 = ["Issue of a service bulletin","Whenever there is an update from the manufacturer, all operators get notified"];
 marketing.m3 = ["Repairing of a broken machine", "Information about how to repari a broken machine can be shared"];


// Marketing Arrays [HEADLINE, TEXT] //
instruction = {}; 
 instruction.i1 = ["place the car on the operator platform"];


//Ccontent
content = '{ "events" : [' +
'{ "marketing":"John" , "lastName":"Doe" },' +
'{ "marketing":"Anna" , "lastName":"Smith" },' +
'{ "marketing":"Peter" , "lastName":"Jones" } ]}';