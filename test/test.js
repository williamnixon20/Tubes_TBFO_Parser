var height = 5;
var radius = 3;
var volume;
// declare and immediately call anonymous function to create scope
(function () {
  var pir2 = Math.PI * radius * radius;  // temp var
  volume = (pir2 * height) / 3;
})();

console.log(volume);
