function addURL() {
    var canvas = document.getElementById("doodle");
    var dataURL = canvas.toDataURL( "image/png" );
    var hiddenel = document.getElementById("hiddenpic");
    hiddenel.value = dataURL;
}
