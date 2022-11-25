var height = 5;
var radius = 3;
var volume;

// declare and immediately call anonymous function to create scope
function blabla() {
    var pir2 = Math.PI * radius * radius; // temp var
    volume = pir2 * height;
}

console.log(volume);
