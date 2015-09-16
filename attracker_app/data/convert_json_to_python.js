//Convert Anand Thakker's centerline-merged.json AT sequenced coordinates to a Python dictionary
// JSON AT map: from atdb.091015051935.ALL.csv at https://github.com/anandthakker/apptrail
// This script was used once to translate centerline-merged.json to at_coordinates.py.
// Subsequently, at_coordinates.py was modified by hand and by script.
var util=require('util')
var fs = require('fs');

var obj = JSON.parse(fs.readFileSync('centerline-merged.json', 'utf8'));
var list = obj['geometry']["coordinates"]

console.log( "Writing ../at_coordinates.py")
var stream = fs.createWriteStream("../at_coordinates.py");
stream.once('open', function(fd) {
    //An approximation to the midpoint of the trail.
    var mid_index = Math.floor(list.length)/2
    stream.write( "# This file is produced by node.js script: convert_json_to_python.js\n" )
    stream.write( util.format("MID = {'lat': %s, 'lng': %s}\n", list[mid_index][1], list[mid_index][0]) );
    stream.write("COORDINATES = [")
    for (var i = 0; i < list.length; i++) {
        stream.write( util.format("  {'lat': %s, 'lng':%s},\n", list[i][1], list[i][0]) );
    }
    stream.write("]\n")
    stream.end();
});

