
var kek = "";
var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

for( var i=0; i < 7; i++ )
{
    kek += possible.charAt(Math.floor(Math.random() * possible.length));
}

var SIZE = 3;
var NAME = kek;


var genHash = function(s) {
    var hash = 0;
    if (s.length === 0) {return hash;}
    for (var i = 0; i < s.length; i++) {
        var char = s.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash;
    }
    return hash;
};
var addZeroes = function(ns, nd) {
    //Shortest useful for loop ever.
    for(;0<nd-ns.length;ns="0"+ns){}return ns;
};
var op = addZeroes(abs(genHash(NAME)).toString(16),8);
debug("hash of "+NAME+" is "+op);
var clr = color(parseInt(op.substring(0,2),16), parseInt(op.substring(2,4),16), parseInt(op.substring(4,6),16));
debug(NAME+"'s color is rgb("+red(clr)+", "+green(clr)+", "+blue(clr)+")");
fill(clr);
noStroke();
randomSeed(parseInt(op.substring(6,8),16));
var mult = 400/((SIZE*2)-1);
for(var x = 0; x < SIZE; x++) {
    for(var y = 0; y < SIZE*2; y++) {
        if(random()<0.5) {
            rect(x*mult,y*mult,mult,mult);
            rect(400-(x+1)*mult,y*mult,mult,mult);
        }
    }
}
